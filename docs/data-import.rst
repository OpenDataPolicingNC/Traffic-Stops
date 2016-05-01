Data Import
===========


Local/Development Environment
-----------------------------


Database Dump (quicker)
_____________________

To load the database dump, run:

.. code-block:: bash

    dropdb traffic_stops_nc
    createdb -E UTF-8 traffic_stops_nc
    wget https://s3-us-west-2.amazonaws.com/openpolicingdata/traffic_stops_nc_production_20150801.tar.zip
    unzip traffic_stops_nc_production_20150801.tar.zip
    pg_restore -Ox -d traffic_stops_nc traffic_stops_nc_production.tar

To create the database dump, run:

.. code-block:: bash

    pg_dump -Ox -Ft traffic_stops > traffic_stops.tar


Raw NC Data (slower)
____________________

Make sure our NC database is in the right state before importing:

.. code-block:: bash

    dropdb traffic_stops_nc && createdb -E UTF-8 traffic_stops_nc
    python manage.py migrate --database=traffic_stops_nc --noinput

Run the import command:

.. code-block:: bash

    python manage.py import_nc --dest $PWD/ncdata

This took ~25 minutes on my laptop. Run ``tail -f traffic_stops.log`` to follow
along.

Now you should be able to view data with ``runserver``:

.. code-block:: bash

    python manage.py runserver


Server
------

Raw NC Data
___________

To start with fresh NC data, first drop the server's database:

.. code-block:: bash

    sudo -u postgres dropdb traffic_stops_nc_staging

Then run a **deploy** to recreate the database.

Temporarily grant our PostgreSQL user SUPERUSER privileges:

.. code-block:: bash

    sudo -u postgres psql -c 'ALTER USER traffic_stops_production WITH SUPERUSER;'

Run the import command:

.. code-block:: bash

    sudo su - traffic_stops
    cd /var/www/traffic-stops
    source ./env/bin/activate
    ./manage.sh import_nc --dest=/var/www/traffic_stops/data

When finished, revoke SUPERUSER privileges:

.. code-block:: bash

    sudo -u postgres psql -c 'ALTER USER traffic_stops_staging WITH NOSUPERUSER;'

Create DB Dump
______________

.. code-block:: bash

    sudo -u postgres pg_dump -Ox -Ft traffic_stops_nc_production > traffic_stops_nc_production.tar
    zip traffic_stops_nc_production.tar.zip traffic_stops_nc_production.tar
    # then on local laptop, run:
    scp opendatapolicingnc.com:traffic_stops_nc_production.tar.zip .
