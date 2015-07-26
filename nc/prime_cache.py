#!/usr/bin/env python
import argparse
import logging
import requests


logger = logging.getLogger(__name__)
ENDPOINTS = ('stops', 'stops_by_reason')


def run(api, host='opendatapolicingnc.com'):
    headers = {'Host': host}
    # get agencies
    r = requests.get(api, headers=headers)
    agencies = r.json()
    for agency in agencies:
        logger.info(agency['name'])
        for endpoint in ENDPOINTS:
            uri = "{}/{}/{}/".format(api.rstrip('/'), agency['id'],
                                     endpoint)
            response = requests.get(uri, headers=headers)
            if response.status_code != 200:
                logging.warning("Status not OK: {} ({})".format(
                                uri, response.status_code))


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('uri', help='Agency REST URI')
    args = parser.parse_args()
    run(args.uri)


if __name__ == "__main__":
    main()
