Data Import 
===========

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
``create-schema.py``:
 
.. code-block:: bash

    time python create-schema.py
    python create-schema.py count

This will create ``data/nc/csv``.

Now use PostgreSQL's ``COPY`` command to load our data:

.. code-block:: bash

    time psql --set=data_dir="$PWD/nc/csv" -f import.sql traffic_stops

.. _csvkit: https://csvkit.readthedocs.org/
