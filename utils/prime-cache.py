#!/usr/bin/env python
import argparse
import logging
import requests


logger = logging.getLogger(__name__)
ENDPOINTS = ('stops', 'stops_by_reason')


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('uri', help='Agency REST URI')
    args = parser.parse_args()
    # get agencies
    r = requests.get(args.uri)
    agencies = r.json()
    for agency in agencies:
        logger.info(agency['name'])
        for endpoint in ENDPOINTS:
            uri = "{}/{}/{}/".format(args.uri.rstrip('/'), agency['id'],
                                     endpoint)
            requests.get(uri)


if __name__ == "__main__":
    main()
