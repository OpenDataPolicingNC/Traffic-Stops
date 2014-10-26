API Endpoints
=============

Stops by all races and ethnicities by year
------------------------------------------

Counts of stops by all races and by all ethnicities by year.


SQL
~~~

Sample SQL query (Durham Police Department):

.. code-block:: sql

    SELECT count(person_id),
           p.race,
           extract(YEAR FROM s.date) AS year
    FROM stops_person p
    JOIN stops_stop s ON p.stop_id = s.stop_id
    WHERE p.type='D'
      AND s.agency_id = 78
    GROUP BY p.race,
             year
    ORDER BY year ASC, p.race DESC;

Sample SQL Results:

.. code-block:: sql

     count | race | year 
    -------+------+------
      4481 | W    | 2005
       357 | U    | 2005
         9 | I    | 2005
      5665 | B    | 2005
       163 | A    | 2005
      5319 | W    | 2006
       231 | U    | 2006
        41 | I    | 2006
      7205 | B    | 2006
       178 | A    | 2006
      7520 | W    | 2007
       120 | U    | 2007
        75 | I    | 2007
     10372 | B    | 2007
       261 | A    | 2007


JSON
~~~~

Sample JSON response (Durham Police Department):

.. code-block:: json

    [
       {
            "year": 2005,
            "native_american": 9,
            "black": 5665,
            "white": 4481,
            "other": 357,
            "non-hispanic": 9298,
            "hispanic": 1377,
            "asian": 163
        },
        {
            "year": 2006,
            "native_american": 41,
            "black": 7200,
            "white": 5318,
            "other": 231,
            "non-hispanic": 11342,
            "hispanic": 1626,
            "asian": 178
        },
        {
            "year": 2007,
            "native_american": 75,
            "black": 10365,
            "white": 7516,
            "other": 120,
            "non-hispanic": 16050,
            "hispanic": 2287,
            "asian": 261
        },
    ]



Likelihood-of-search by stop-reason
-----------------------------------

A count of likelihood-of-search by stop-reason.


SQL Query
~~~~~~~~~

One query for all stops and another for only stops with searches.

.. code-block:: sql

    SELECT count(p.person_id),
           p.race,
           s.purpose,
           extract(YEAR FROM s.date) AS year
    FROM stops_person p
    JOIN stops_stop s ON p.stop_id = s.stop_id
    WHERE p.type='D'
      AND s.agency_id = 78
    GROUP BY p.race,
             s.purpose,
             year
    ORDER BY year ASC,
             s.purpose ASC,
             p.race DESC;

    SELECT count(se.person_id),
           p.race,
           s.purpose,
           extract(YEAR FROM s.date) AS year
    FROM stops_person p
    JOIN stops_stop s ON p.stop_id = s.stop_id
    JOIN stops_search se ON s.stop_id = se.stop_id
    WHERE p.type='D'
      AND s.agency_id = 78
    GROUP BY p.race,
             s.purpose,
             year
    ORDER BY year ASC,
             s.purpose ASC,
             p.race DESC;

Sample SQL Results:

.. code-block:: sql

     count | race | purpose | year 
    -------+------+---------+------
      2568 | W    |       1 | 2006
       134 | U    |       1 | 2006
        31 | I    |       1 | 2006
      2386 | B    |       1 | 2006
       117 | A    |       1 | 2006
       272 | W    |       2 | 2006
        18 | U    |       2 | 2006
       348 | B    |       2 | 2006
         8 | A    |       2 | 2006
        29 | W    |       3 | 2006
        35 | B    |       3 | 2006
       342 | W    |       4 | 2006
         9 | U    |       4 | 2006
         1 | I    |       4 | 2006
       430 | B    |       4 | 2006
        11 | A    |       4 | 2006
       628 | W    |       5 | 2006
        14 | U    |       5 | 2006
         3 | I    |       5 | 2006
      1231 | B    |       5 | 2006
        12 | A    |       5 | 2006
       750 | W    |       6 | 2006
        20 | U    |       6 | 2006
         4 | I    |       6 | 2006
      1511 | B    |       6 | 2006
        11 | A    |       6 | 2006
       198 | W    |       7 | 2006
         9 | U    |       7 | 2006
       373 | B    |       7 | 2006
         5 | A    |       7 | 2006
       204 | W    |       8 | 2006
         3 | U    |       8 | 2006
       409 | B    |       8 | 2006
         1 | A    |       8 | 2006
       328 | W    |       9 | 2006
        24 | U    |       9 | 2006
         2 | I    |       9 | 2006
       482 | B    |       9 | 2006
        13 | A    |       9 | 2006

     count | race | purpose | year 
    -------+------+---------+------
        73 | W    |       1 | 2006
         1 | U    |       1 | 2006
       126 | B    |       1 | 2006
         5 | A    |       1 | 2006
        21 | W    |       2 | 2006
         1 | U    |       2 | 2006
        25 | B    |       2 | 2006
        19 | W    |       3 | 2006
        18 | B    |       3 | 2006
        44 | W    |       4 | 2006
        56 | B    |       4 | 2006
        62 | W    |       5 | 2006
       156 | B    |       5 | 2006
         1 | A    |       5 | 2006
        47 | W    |       6 | 2006
         1 | U    |       6 | 2006
       169 | B    |       6 | 2006
         5 | W    |       7 | 2006
         1 | U    |       7 | 2006
        26 | B    |       7 | 2006
        29 | W    |       8 | 2006
        91 | B    |       8 | 2006
         1 | A    |       8 | 2006
        16 | W    |       9 | 2006
         2 | U    |       9 | 2006
         1 | I    |       9 | 2006
        50 | B    |       9 | 2006


JSON Response
~~~~~~~~~~~~~

.. code-block:: json

    {
        "searches": [
            {
                "purpose": 1,
                "year": 2006,
                "hispanic": 35,
                "native_american": 0,
                "white": 73,
                "asian": 5,
                "black": 126,
                "non-hispanic": 170,
                "other": 1
            },
            {
                "purpose": 2,
                "year": 2006,
                "hispanic": 14,
                "native_american": 0,
                "white": 21,
                "asian": 0,
                "black": 25,
                "non-hispanic": 33,
                "other": 1
            }
        ],
        "stops": [
            {
                "purpose": 1,
                "year": 2006,
                "hispanic": 475,
                "native_american": 31,
                "white": 2567,
                "asian": 117,
                "black": 2386,
                "non-hispanic": 4760,
                "other": 134
            },
            {
                "purpose": 2,
                "year": 2006,
                "hispanic": 90,
                "native_american": 0,
                "white": 272,
                "asian": 8,
                "black": 348,
                "non-hispanic": 556,
                "other": 18
            },
        ]
    }


Use-of-force
------------

A count of all use-of-force by all races and by all ethnicities by year.


SQL Query
~~~~~~~~~

Sample SQL query:

.. code-block:: sql

    SELECT count(se.person_id),
           p.race,
           extract(YEAR FROM s.date) AS year
    FROM stops_person p
    JOIN stops_stop s ON p.stop_id = s.stop_id
    JOIN stops_search se ON s.stop_id = se.stop_id
    WHERE p.type='D'
      AND s.agency_id = 78
      AND s.engage_force = 't'
    GROUP BY p.race,
             year
    ORDER BY p.race DESC,
             year ASC;

Sample SQL results:

.. code-block:: sql

     count | race | year 
    -------+------+------
         3 | W    | 2002
         1 | W    | 2003
         1 | W    | 2005
         3 | W    | 2006
         3 | W    | 2007
         9 | W    | 2008
         1 | W    | 2010
         1 | W    | 2011
         1 | W    | 2012
         2 | U    | 2002
        12 | B    | 2002
         4 | B    | 2003
         4 | B    | 2004
         1 | B    | 2005
         5 | B    | 2006
        10 | B    | 2007
        12 | B    | 2008
         3 | B    | 2009
         4 | B    | 2010
         8 | B    | 2011
         4 | B    | 2012
         1 | B    | 2013
    (22 rows)


JSON
~~~~

Sample JSON response (Durham Police Department):

.. code-block:: json

    [
        {
            "year": 2006,
            "native_american": 0,
            "other": 0,
            "black": 5,
            "hispanic": 3,
            "asian": 0,
            "non-hispanic": 5,
            "white": 3
        },
        {
            "year": 2007,
            "native_american": 0,
            "other": 0,
            "black": 10,
            "hispanic": 1,
            "asian": 0,
            "non-hispanic": 12,
            "white": 3
        },
        {
            "year": 2008,
            "native_american": 0,
            "other": 0,
            "black": 12,
            "hispanic": 6,
            "asian": 0,
            "non-hispanic": 15,
            "white": 9
        }
    ]


Contraband Hit Rate (Not working)
---------------------------------

A count of contraband hit-rate by race, year, and search-type. I'm not sure


SQL Query
~~~~~~~~~

One query for all stops with searches and another for stops with searches with contraband.

.. code-block:: sql

    SELECT count(se.person_id),
           p.race,
           se.type,
           extract(YEAR FROM s.date) AS year
    FROM stops_person p
    JOIN stops_stop s ON p.stop_id = s.stop_id
    JOIN stops_search se ON s.stop_id = se.stop_id
    WHERE p.type='D'
      AND s.agency_id = 78
    GROUP BY p.race,
             se.type,
             year
    ORDER BY year ASC,
             se.type ASC,
             p.race DESC;

    SELECT count(c.person_id),
           p.race,
           extract(YEAR FROM s.date) AS year
    FROM stops_person p
    JOIN stops_stop s ON p.stop_id = s.stop_id
    JOIN stops_search se ON s.stop_id = se.stop_id
    JOIN stops_contraband c ON se.search_id = c.search_id
     AND p.person_id = c.person_id
     AND se.stop_id = c.stop_id
    WHERE p.type='D'
      AND s.agency_id = 78
    GROUP BY p.race,
             s.purpose,
             year
    ORDER BY year ASC,
             p.race DESC;

Sample SQL Results:

.. code-block:: sql

     count | race | purpose | year 
    -------+------+---------+------
        73 | W    |       1 | 2006
         1 | U    |       1 | 2006
       126 | B    |       1 | 2006
         5 | A    |       1 | 2006
        21 | W    |       2 | 2006
         1 | U    |       2 | 2006
        25 | B    |       2 | 2006
        19 | W    |       3 | 2006
        18 | B    |       3 | 2006
        44 | W    |       4 | 2006
        56 | B    |       4 | 2006
        62 | W    |       5 | 2006
       156 | B    |       5 | 2006
         1 | A    |       5 | 2006
        47 | W    |       6 | 2006
         1 | U    |       6 | 2006
       169 | B    |       6 | 2006
         5 | W    |       7 | 2006
         1 | U    |       7 | 2006
        26 | B    |       7 | 2006
        29 | W    |       8 | 2006
        91 | B    |       8 | 2006
         1 | A    |       8 | 2006
        16 | W    |       9 | 2006
         2 | U    |       9 | 2006
         1 | I    |       9 | 2006
        50 | B    |       9 | 2006
