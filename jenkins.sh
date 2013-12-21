#!/bin/sh -ex

export LC_ALL=en_US.UTF-8

# See where we came from:
git remote -v

# Create a clean test env
rm -f .coverage
rm -rf env
find . -name "*.pyc" -exec rm -rf {} \;
virtualenv -q --clear --python=/usr/bin/python2.7 env
. env/bin/activate
pip install -q -r requirements/dev.txt

# Run the tests
./run_tests.sh --noinput
