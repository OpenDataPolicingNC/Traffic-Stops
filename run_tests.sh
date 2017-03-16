#!/bin/sh
set -ex

# MIN_COVERAGE should match the value in .travis.yml
MIN_COVERAGE=74

if test "$1" = "--nokeepdb"; then
    DBARG=""
    shift
else
    DBARG="--keepdb"
fi

# Check PEP-8
flake8 .

rm -f .coverage
coverage run manage.py test ${DBARG} --noinput --settings=traffic_stops.settings.dev "$@"
coverage report --fail-under=${MIN_COVERAGE}

python manage.py makemigrations --dry-run | grep 'No changes detected' || (echo 'There are changes which require migrations.' && exit 1)
