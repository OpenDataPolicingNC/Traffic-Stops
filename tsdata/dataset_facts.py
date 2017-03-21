import math

from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Count
from memoize import delete_memoized, memoize
import pytz

from .models import StateFacts, TopAgencyFacts


@memoize(timeout=300)
def get_dataset_facts_context():
    context = {}
    for state_facts in StateFacts.objects.all():
        context[state_facts.state_key] = state_facts
    return context


def compute_dataset_facts(
        Agency, Stop, state_key, Search=None,
        override_start_date=None):
    """
    Compute dataset facts for a state, as used on the home page and on
    state-specific landing pages.

    The facts will be stored in the database (StateFacts and TopAgencyFacts
    models), and a printable form will be returned for display by management
    commands.

    This code requires that StateFacts and TopAgencyFacts instances already
    exist for the state, as the existing ones will be updated instead of
    creating more.

    :param Agency: the state's Agency model (class)
    :param Stop: the state's Stop model (class)
    :param state_key: one of settings.IL_KEY, settings.MD_KEY, etc.
    :param Search: the state's Search model (class), if it has one
    :param override_start_date: text to use instead of the computed start date
      (NC has little data for 2000-2001 and pretends for display purposes that
      the data starts in 2002)
    :return: printable form of the data
    """
    state_config = settings.STATE_CONFIG[state_key]
    state_tz = pytz.timezone(state_config.tz_name)

    try:
        Stop._meta.get_field('date')
        first_stop = Stop.objects.all().order_by('date').first()
        last_stop = Stop.objects.all().order_by('-date').first()
        time_fmt = '%b %d, %Y'
        first_stop_time = first_stop.date.astimezone(state_tz)
        first_stop_time_str = first_stop_time.strftime(time_fmt)
        last_stop_time = last_stop.date.astimezone(state_tz)
        last_stop_time_str = last_stop_time.strftime(time_fmt)
    except FieldDoesNotExist:
        first_stop = Stop.objects.all().order_by('year').first()
        last_stop = Stop.objects.all().order_by('-year').first()
        first_stop_time = first_stop.year
        first_stop_time_str = str(first_stop_time)
        last_stop_time = last_stop.year
        last_stop_time_str = str(last_stop_time)

    if override_start_date is not None:
        first_stop_time_str = override_start_date

    if Search is not None:
        search_count = Search.objects.count()
    else:
        search_count = Stop.objects.filter(search_conducted='Y').count()

    total_stops = Stop.objects.count()
    StateFacts.objects.filter(state_key=state_key).update(
        total_stops=total_stops,
        total_stops_millions=math.floor(total_stops / 1000000),
        total_searches=search_count,
        total_agencies=Agency.objects.count(),
        start_date=first_stop_time_str,
        end_date=last_stop_time_str,
    )
    state_facts = StateFacts.objects.get(state_key=state_key)

    facts = [
        'Timeframe: %s - %s' % (first_stop_time_str, last_stop_time_str),
        'Stops: {:,}'.format(state_facts.total_stops),
        'Searches: {:,}'.format(state_facts.total_searches),
        'Agencies: {:,}'.format(state_facts.total_agencies),
        '',
        'Top 5:',
    ]

    top_agencies = Agency.objects.annotate(num_stops=Count('stops')).order_by('-num_stops')[:5]
    rank = 1
    for agency in top_agencies:
        facts.append('Id {}: {} {:,}'.format(agency.id, agency.name, agency.num_stops))
        TopAgencyFacts.objects.filter(state_facts=state_facts, rank=rank).update(
            agency_id=agency.id,
            stops=agency.num_stops,
            name=agency.name,
        )
        rank += 1

    # Dev consideration when using LocMemCache backend:
    # This only changes lookups used in the same process.
    delete_memoized(get_dataset_facts_context)
    get_dataset_facts_context()

    return facts
