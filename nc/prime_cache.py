import logging
import time
import urllib

from django.core.urlresolvers import reverse
from django.db.models import Count
from django.test.client import Client
import requests

from nc.models import Agency

logger = logging.getLogger(__name__)
ENDPOINTS = ('stops', 'stops_by_reason', 'use_of_force', 'searches', 'contraband_hit_rate')


def run(root, host=None):
    remote = False
    agencies = [
        (a.id, a.name)
        for a in Agency.objects.annotate(num_stops=Count('stops')).order_by('-num_stops')
    ]
    headers = dict()
    if host is not None:
        headers['Host'] = host
    if remote:
        api = urllib.parse.urljoin(root, reverse('nc:agency-api-list'))
    else:
        api = reverse('nc:agency-api-list')
    # # get agencies
    # r = requests.get(api, headers=headers)
    # agencies = r.json()
    # for agency in agencies:
    for agency_id, agency_name in agencies:
        logger.info(agency_name)
        elapsed = []
        # prime each API endpoint
        for endpoint in ENDPOINTS:
            uri = "{}/{}/{}/".format(api.rstrip('/'), agency_id,
                                     endpoint)
            start_time = time.time()
            req(uri, headers=headers)
            elapsed.append(time.time() - start_time)
        # prime first search page
        payload = {'agency': agency_name}
        search_uri = urllib.parse.urljoin(root, reverse('nc:stops-search'))
        start_time = time.time()
        req(search_uri, headers, payload)
        elapsed.append(time.time() - start_time)
        elapsed = sum(elapsed)
        print(elapsed, agency_id, agency_name)


def req(uri, headers, payload=None, remote=False):
    if remote:
        try:
            response = requests.get(uri, headers=headers, params=payload)
            if response.status_code != 200:
                logger.warning("Status not OK: {} ({})".format(
                               uri, response.status_code))
        except requests.ConnectionError as err:
            logger.error('Cannot load %s: %s', uri, err)
            response = None
        return response
    else:
        c = Client()
        response = c.get(uri, data=payload, HTTP_HOST='127.0.0.1')
        if response.status_code != 200:
            logger.warning("Status not OK: {} ({})".format(
                           uri, response.status_code))
            raise Exception('Request to %s failed: %s', uri, response.status_code)
        return response
