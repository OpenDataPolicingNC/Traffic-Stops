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

Basic SQL query:

.. code-block:: sql

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
    ORDER BY s.purpose ASC,
             p.race DESC,
             year ASC;


JSON Response
~~~~~~~~~~~~~

.. code-block:: json

    {
      stops: [
        {reason: 'Speed Limit Violation', year: 2010, black: 10, white:10, asian: 10, native_american:10, other:10, hispanic: 10, nonhispanic: 10},
        {reason: 'Stop Light/Sign Violation', year: 2010, black: 10, white:10, asian: 10, native_american:10, other:10, hispanic: 10, nonhispanic: 10},
        {reason: 'Driving While Impaired', year: 2011, black: 10, white:10, asian: 10, native_american:10, other:10, hispanic: 10, nonhispanic: 10}
      ],
      searches: [
        {reason: 'Speed Limit Violation', year: 2010, black: 10, white:10, asian: 10, native_american:10, other:10, hispanic: 10, nonhispanic: 10},
        {reason: 'Stop Light/Sign Violation', year: 2010, black: 10, white:10, asian: 10, native_american:10, other:10, hispanic: 10, nonhispanic: 10},
        {reason: 'Driving While Impaired', year: 2011, black: 10, white:10, asian: 10, native_american:10, other:10, hispanic: 10, nonhispanic: 10}
      ]
    }
