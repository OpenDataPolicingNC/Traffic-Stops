#!/bin/sh -ex

# Check PEP-8
if ! flake8 traffic_stops ; then
  echo "PEP-8 checking failed"
  exit 1
fi

coverage run manage.py test  --settings=traffic_stops.settings.dev "$@" && coverage report
