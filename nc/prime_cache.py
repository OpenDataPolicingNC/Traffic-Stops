#!/usr/bin/env python
import argparse
import logging
import requests
import urllib

from django.core.urlresolvers import reverse


logger = logging.getLogger(__name__)
ENDPOINTS = ('stops', 'stops_by_reason', 'use_of_force', 'searches', 'contraband_hit_rate')


def run(root, host='opendatapolicingnc.com'):
    headers = {'Host': host}
    api = urllib.parse.urljoin(root, reverse('agency-api-list'))
    # get agencies
    r = requests.get(api, headers=headers)
    agencies = r.json()
    for agency in agencies:
        logger.info(agency['name'])
        # prime each API endpoint
        for endpoint in ENDPOINTS:
            uri = "{}/{}/{}/".format(api.rstrip('/'), agency['id'],
                                     endpoint)
            req(uri, headers=headers)
        # prime first search page
        payload = {'agency': agency['name']}
        search_uri = urllib.parse.urljoin(root, reverse('stops-search'))
        req(search_uri, headers, payload)


def req(uri, headers, payload=None):
    try:
        response = requests.get(uri, headers=headers, params=payload)
    except requests.ConnectionError as err:
        logger.error(err)
    if response.status_code != 200:
        logger.warning("Status not OK: {} ({})".format(
                       uri, response.status_code))
    return response


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('uri', help='Root URL (e.g. http://0.0.0.0:8000/)')
    args = parser.parse_args()
    run(args.uri)


if __name__ == "__main__":
    main()
