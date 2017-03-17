import logging
import time

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.test.client import Client

from nc.models import Agency

logger = logging.getLogger(__name__)
ENDPOINTS = ('stops', 'stops_by_reason', 'use_of_force', 'searches', 'contraband_hit_rate')
DEFAULT_CUTOFF_SECS = 4


def run(cutoff_duration_secs=None):
    """
    Prime query cache for "big" NC agencies.

    Order the agencies by number of stops, and keep making the web requests
    that use the queries until the queries for an agency take less than
    cutoff_duration_secs.

    This is expected to be used as part of the following flow:
    1. reload new NC data
    2. flush memcached
    3. prime the cache to load the new data into the query cache

    If memcached isn't flushed before priming the cache, this function will
    presumably exit prematurely without loading the new data.

    This uses the Django test client to avoid encountering Gunicorn timeouts,
    so it can't be used remotely.

    :param cutoff_duration_secs: Once priming the cache for an agency takes
    less than this, stop.
    """
    if cutoff_duration_secs is None:
        cutoff_duration_secs = DEFAULT_CUTOFF_SECS
    logger.info('NC prime_cache starting')
    agencies = [
        (a.id, a.name, a.num_stops)
        for a in Agency.objects.annotate(num_stops=Count('stops')).order_by('-num_stops')
    ]
    api = reverse('nc:agency-api-list')
    agencies_processed = 0
    for agency_id, agency_name, num_stops in agencies:
        elapsed = []  # collect times for each request
        # prime each API endpoint
        for endpoint in ENDPOINTS:
            uri = "{}/{}/{}/".format(api.rstrip('/'), agency_id,
                                     endpoint)
            start_time = time.time()
            req(uri)
            elapsed.append(time.time() - start_time)
        # prime first search page
        payload = {'agency': agency_name}
        search_uri = reverse('nc:stops-search')
        start_time = time.time()
        req(search_uri, payload)
        elapsed.append(time.time() - start_time)
        elapsed = sum(elapsed)
        logger.info('Primed cache for agency %s:%s with %s stops in %.2f secs',
                    agency_id, agency_name, '{:,}'.format(num_stops), elapsed)
        agencies_processed += 1
        num_remaining_agencies = len(agencies) - agencies_processed
        if elapsed < cutoff_duration_secs and num_remaining_agencies > 0:
            logger.info('Not priming cache for %s remaining agencies',
                        num_remaining_agencies)
            break


def req(uri, payload=None):
    c = Client()
    if settings.ALLOWED_HOSTS and settings.ALLOWED_HOSTS[0] != '*':
        host = settings.ALLOWED_HOSTS[0]
    else:
        host = '127.0.0.1'
    response = c.get(uri, data=payload, HTTP_HOST=host)
    if response.status_code != 200:
        logger.warning("Status not OK: {} ({})".format(
                       uri, response.status_code))
        raise Exception('Request to %s failed: %s', uri, response.status_code)
