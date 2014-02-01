NC Traffic Stops
================

Below you will find basic setup and deployment instructions for the NC Traffic Stops
project. To begin you should have the following applications installed on your
local development system:

- Python 2.7
- `pip >= 1.4 <http://www.pip-installer.org/>`_
- `virtualenv >= 1.10 <http://www.virtualenv.org/>`_
- `virtualenvwrapper >= 3.0 <http://pypi.python.org/pypi/virtualenvwrapper>`_
- Postgres >= 9.1
- git >= 1.7

The deployment uses SSH with agent forwarding so you'll need to enable agent
forwarding if it is not already by adding ``ForwardAgent yes`` to your SSH config.


Getting Started
------------------------

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    mkvirtualenv nc-traffic-stops
    $VIRTUAL_ENV/bin/pip install -r $PWD/requirements/dev.txt

Then create a local settings file and set your ``DJANGO_SETTINGS_MODULE`` to
use it::

    cp traffic_stops/settings/local.example.py traffic_stops/settings/local.py
    echo "export DJANGO_SETTINGS_MODULE=traffic_stops.settings.local" >> $VIRTUAL_ENV/bin/postactivate
    echo "unset DJANGO_SETTINGS_MODULE" >> $VIRTUAL_ENV/bin/postdeactivate

Exit the virtualenv and reactivate it to activate the settings just changed::

    deactivate
    workon nc-traffic-stops

Create the Postgres database and run the initial syncdb/migrate::

    createdb -E UTF-8 traffic_stops
    python manage.py syncdb
    python manage.py migrate

You should now be able to run the development server::

    python manage.py runserver
