Data Import
===========

Stop data is imported in the same manner for all states.  Substitute the state
abbreviation (e.g., "md") as appropriate in the NC instructions below.

Census data for all states is imported all at once, in the same manner for all
environments, using the ``import_census`` management command.  This must be
performed as part of developer and server setup as well as when additional states
are added.

Local/Development Environment
-----------------------------


Database Dump (quicker)
_______________________

To load an existing database dump on S3, run:

.. code-block:: bash

    dropdb traffic_stops_nc
    createdb -E UTF-8 traffic_stops_nc
    wget https://s3-us-west-2.amazonaws.com/openpolicingdata/traffic_stops_nc_production_20150801.tar.zip
    unzip traffic_stops_nc_production_20150801.tar.zip
    pg_restore -Ox -d traffic_stops_nc traffic_stops_nc_production.tar

Browse https://s3-us-west-2.amazonaws.com/openpolicingdata/ to see what dumps
are available.

To create a new database dump, run:

.. code-block:: bash

    pg_dump -Ox -Ft traffic_stops > traffic_stops.tar

That can be loaded with the ``pg_restore`` command shown above.

Raw NC Data (slower)
____________________

The state-specific database must exist and current migrations need to have been
applied before importing.  If in doubt:

.. code-block:: bash

    dropdb traffic_stops_nc && createdb -E UTF-8 traffic_stops_nc
    python manage.py migrate --database=traffic_stops_nc --noinput

Command-line
++++++++++++

Run the import command:

.. code-block:: bash

    python manage.py import_nc --dest $PWD/ncdata

This took ~25 minutes on my laptop. Run ``tail -f traffic_stops.log`` to follow
along.  Reusing an existing ``--dest`` directory will speed up import.  However,
if import code has changed since the last time the directory was used, don't
reuse an existing directory.

Now you should be able to view data with ``runserver``:

.. code-block:: bash

    python manage.py runserver

Admin
+++++

Access /admin/tsdata/dataset/ and create a "dataset" describing the data to be
imported.  Setting the fields:

- Select the desired state
- Provide a unique name for the dataset
- The date received should reflect when the raw data was received
- Set the URL to one of the available datasets at
  https://s3-us-west-2.amazonaws.com/openpolicingdata/ .  The normal URLs
  are stored in the source code (in ``<state_app>.data.__init__.py``).
- Specify a destination directory where the dataset will be downloaded and
  extracted.

Once the "dataset" has been created, select the new dataset in list view and
apply the "Import selected dataset" action.

Server
------

The PostgreSQL user must have SUPERUSER privileges to perform the import.
Depending on current admin policies, that may have to be granted and
revoked around the import.

Temporarily grant our PostgreSQL user SUPERUSER privileges:

.. code-block:: bash

    sudo -u postgres psql -c 'ALTER USER traffic_stops_staging WITH SUPERUSER;'

When finished, revoke SUPERUSER privileges:

.. code-block:: bash

    sudo -u postgres psql -c 'ALTER USER traffic_stops_staging WITH NOSUPERUSER;'

After importing new state data into the database used by a running server,
cached queries will continue to be used until they expire.  To flush the
cache, connect to ``memcached`` using ``telnet`` or some other suitable
client and send the ``flush_all`` command.

Raw NC Data
___________

Command-line
++++++++++++

Run the import command:

.. code-block:: bash

    sudo su - traffic_stops
    cd /var/www/traffic_stops
    source ./env/bin/activate
    ./manage.sh import_nc --dest=/var/www/traffic_stops/data

Reusing an existing ``--dest`` directory will speed up import.  However,
if import code has changed since the last time the directory was used, don't
reuse an existing directory.

Admin
+++++

Follow the "Admin" instructions above under "Local/Development Environment".

Create DB Dump
______________

.. code-block:: bash

    sudo -u postgres pg_dump -Ox -Ft traffic_stops_nc_production > traffic_stops_nc_production.tar
    zip traffic_stops_nc_production.tar.zip traffic_stops_nc_production.tar
    # then on local laptop, run:
    scp opendatapolicingnc.com:traffic_stops_nc_production.tar.zip .
