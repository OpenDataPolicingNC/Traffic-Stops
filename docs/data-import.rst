Data Import 
===========


Database Dump
-------------

To load the database dump, run:

.. code-block:: bash

    sudo -u postgres dropdb traffic_stops_production
    sudo -u postgres createdb -O traffic_stops_production traffic_stops_production
    sudo -u postgres pg_restore --role=traffic_stops_production -Oxa -d traffic_stops_production /var/www/traffic_stops/traffic_stops.tar

To create the database dump, run:

.. code-block:: bash

    pg_dump -Ox -Ft traffic_stops > traffic_stops.tar


Raw Data
--------

Make sure our database is in the right state before importing:

.. code-block:: bash

    dropdb traffic_stops;
    createdb -E UTF-8 traffic_stops
    python manage.py syncdb --noinput
    python manage.py migrate stops 0001

Download the extract the latest North Carolina data dump into
``<git-repo>/data/nc``.

.. code-block:: bash

    cd data/
    unzip -d nc raw-data.zip
    sudo chmod 666 nc/*

Convert space-delineated files to CSVs with the help of `csvkit`_ and 
``create-schema.py`` (this will create ``data/nc/csv``):
 
.. code-block:: bash

    time python create-schema.py
    python create-schema.py count

The output will show the line counts of each file. The CSV files should have an
extra line for the header.

.. code-block:: bash

    (nc-traffic-stops)copelco@caktus005:~/projects/nc-traffic-stop/data$ python create-schema.py count
    CONTRABAND
    DAT 136346
    CSV 136347
    REFCOMMONCODE
    DAT 218
    CSV 219
    SEARCH
    DAT 542736
    CSV 542737
    SEARCHBASIS
    DAT 618871
    CSV 618872
    REFSTOPSCODENUMBER
    DAT 28
    CSV 29
    REFCODETYPE
    DAT 17
    CSV 18
    STOP
    DAT 16822954
    CSV 16822955
    PERSON
    DAT 17108280
    CSV 17108281

Now use PostgreSQL's ``COPY`` command to load our data:

.. code-block:: bash

    time psql --set=data_dir="$PWD/nc/csv" -f import.sql traffic_stops

This took ~25 minutes on my laptop. The output should match the line count from
above:

.. code-block:: bash

    BEGIN
    psql:import.sql:18: NOTICE:  truncate cascades to table "stops_contraband"
    psql:import.sql:18: NOTICE:  truncate cascades to table "stops_person"
    psql:import.sql:18: NOTICE:  truncate cascades to table "stops_search"
    psql:import.sql:18: NOTICE:  truncate cascades to table "stops_searchbasis"
    TRUNCATE TABLE
    ANALYZE
    COMMIT
    BEGIN
    COPY 16822954
    COMMIT
    BEGIN
    COPY 17108280
    COMMIT
    BEGIN
    COPY 542736
    COMMIT
    BEGIN
    COPY 136346
    COMMIT
    BEGIN
    COPY 618871
    COMMIT
    BEGIN
    ANALYZE
    COMMIT

    real    25m42.752s
    user    0m0.036s
    sys 0m0.012s

Apply the latest migrations:

.. code-block:: bash

    python manage.py syncdb --noinput

Now you should be able to view data with ``runserver``:

.. code-block:: bash

    python manage.py runserver


.. _csvkit: https://csvkit.readthedocs.org/
