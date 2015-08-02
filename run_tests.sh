#!/bin/sh
set -ex

# Check PEP-8
# flake8 .

rm -f .coverage
coverage run manage.py test --noinput --settings=traffic_stops.settings.dev "$@"
coverage report
