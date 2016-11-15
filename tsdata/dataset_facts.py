from django.core.exceptions import FieldDoesNotExist
from django.db.models import Count
import pytz


def compute_dataset_facts(Agency, Stop, state_tz_name, Search=None):
    state_tz = pytz.timezone(state_tz_name)

    try:
        Stop._meta.get_field('date')
        first_stop = Stop.objects.all().order_by('date').first()
        last_stop = Stop.objects.all().order_by('-date').first()
        time_fmt = '%b %d, %Y'
        first_stop_time = first_stop.date.astimezone(state_tz).strftime(time_fmt)
        last_stop_time = last_stop.date.astimezone(state_tz).strftime(time_fmt)
    except FieldDoesNotExist:
        first_stop = Stop.objects.all().order_by('year').first()
        last_stop = Stop.objects.all().order_by('-year').first()
        first_stop_time = first_stop.year
        last_stop_time = last_stop.year

    if Search is not None:
        search_count = Search.objects.count()
    else:
        search_count = Stop.objects.filter(search_conducted='Y').count()

    facts = [
        'Timeframe: %s - %s' % (first_stop_time, last_stop_time),
        'Stops: {:,}'.format(Stop.objects.count()),
        'Searches: {:,}'.format(search_count),
        'Agencies: {:,}'.format(Agency.objects.count()),
        '',
        'Top 5:',
    ]

    top_agencies = Agency.objects.annotate(num_stops=Count('stops')).order_by('-num_stops')[:5]
    for agency in top_agencies:
        facts.append('Id {}: {} {:,}'.format(agency.id, agency.name, agency.num_stops))

    return facts
