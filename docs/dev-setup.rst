Development Setup
=================

Below you will find basic setup and deployment instructions for the NC Traffic
Stops project. To begin you should have the following applications installed on
your local development system:

- Python 3.4 or 3.5
- NodeJS >= 4.2
- `pip >= 9.0.1 <http://www.pip-installer.org/>`_
- `virtualenv >= 1.10 <http://www.virtualenv.org/>`_
- `virtualenvwrapper >= 3.0 <http://pypi.python.org/pypi/virtualenvwrapper>`_
- Postgres >= 9.3
- git >= 1.7

If you need Python 3.4 installed, you can use this PPA::

    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get update
    sudo apt-get install python3.4-dev

(If you build Python 3.4 yourself on Ubuntu, ensure that the `libbz2-dev`
package is installed first.)

The tool that we use to deploy code is called `Fabric
<http://docs.fabfile.org/>`_, which is not yet Python3 compatible. So,
we need to install that globally in our Python2 environment::

    sudo pip install fabric==1.10.0

The deployment uses SSH with agent forwarding so you'll need to enable agent
forwarding if it is not already by adding ``ForwardAgent yes`` to your SSH
config.


Getting Started
---------------

To setup your local environment you should create a virtualenv and install the
necessary requirements::

    $ which python3.4  # make sure you have Python 3.4 installed
    $ mkvirtualenv --python=`which python3.4` opendatapolicing
    (opendatapolicing)$ pip install -U pip
    (opendatapolicing)$ pip install -r requirements/dev.txt
    (opendatapolicing)$ npm install

Next, we'll set up our local environment variables. We use `django-dotenv
<https://github.com/jpadilla/django-dotenv>`_ to help with this. It reads environment variables
located in a file name ``.env`` in the top level directory of the project. The only variable we need
to start is ``DJANGO_SETTINGS_MODULE``::

    (opendatapolicing)$ cp traffic_stops/settings/local.example.py traffic_stops/settings/local.py
    (opendatapolicing)$ echo "DJANGO_SETTINGS_MODULE=traffic_stops.settings.local" > .env

Exit the virtualenv and reactivate it to activate the settings just changed::

    (opendatapolicing)$ deactivate
    (opendatapolicing)$ workon opendatapolicing

Create the Postgres database and run the initial syncdb/migrate::

    (opendatapolicing)$ createdb -E UTF-8 traffic_stops
    (opendatapolicing)$ createdb -E UTF-8 traffic_stops_nc
    (opendatapolicing)$ createdb -E UTF-8 traffic_stops_md
    (opendatapolicing)$ createdb -E UTF-8 traffic_stops_il
    (opendatapolicing)$ ./migrate_all_dbs.sh

Development
-----------

You should be able to run the development server via the configured ``dev`` script::

    (opendatapolicing)$ npm run dev

Or, on a custom port and address::

    (opendatapolicing)$ npm run dev -- --address=0.0.0.0 --port=8020

Any changes made to Python, Javascript or Less files will be detected and rebuilt transparently as
long as the development server is running.

When running migrations
-----------------------

This is a multi-database project.  Whenever you have unapplied migrations,
either added locally or via an update from the source repository, the
migrations need to be applied to all databases by running the
``./migrate_all_dbs.sh`` command.
