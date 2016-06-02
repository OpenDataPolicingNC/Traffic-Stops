-- psql -f materialized_view.sql traffic_stops_nc

BEGIN;

DROP MATERIALIZED VIEW IF EXISTS computed_annual_stats;
DROP SEQUENCE IF EXISTS computed_annual_stats_pkey_seq;

-- http://gis.stackexchange.com/questions/12233/in-postgis-is-it-possible-to-create-a-view-with-a-unique-id
CREATE SEQUENCE computed_annual_stats_pkey_seq CYCLE;

CREATE MATERIALIZED VIEW computed_annual_stats
AS
SELECT nextval('computed_annual_stats_pkey_seq'::regclass) AS id,
       s.agency_id,
       EXTRACT(YEAR FROM s.date) AS year,
       s.officer_id,
       p.race,
       s.purpose,
       s.engage_force AS use_of_force,
       COUNT(p.person_id) AS stops,
       COUNT(se.search_id) AS searches
FROM nc_person p
JOIN nc_stop s ON p.stop_id = s.stop_id
LEFT OUTER JOIN nc_search se ON s.stop_id = se.stop_id
WHERE p.type='D'
  -- AND s.agency_id = 79
GROUP BY s.agency_id,
         year,
         s.officer_id,
         p.race,
         use_of_force,
         s.purpose

UNION

SELECT nextval('computed_annual_stats_pkey_seq'::regclass) AS id,
       s.agency_id,
       EXTRACT(YEAR FROM s.date) AS year,
       s.officer_id,
       p.ethnicity AS race,
       s.purpose,
       s.engage_force AS use_of_force,
       COUNT(p.person_id) AS stops,
       COUNT(se.search_id) AS searches
FROM nc_person p
JOIN nc_stop s ON p.stop_id = s.stop_id
LEFT OUTER JOIN nc_search se ON s.stop_id = se.stop_id
WHERE p.type='D'
  -- AND s.agency_id = 79
GROUP BY s.agency_id,
         year,
         s.officer_id,
         p.ethnicity,
         use_of_force,
         s.purpose
-- ORDER BY year ASC,
--          s.officer_id,
--          s.purpose ASC,
--          p.race DESC


WITH DATA;

CREATE UNIQUE INDEX ON computed_annual_stats USING btree (id);
CREATE INDEX ON computed_annual_stats USING btree (agency_id);
CREATE INDEX ON computed_annual_stats USING btree (year);
CREATE INDEX ON computed_annual_stats USING btree (officer_id);
CREATE INDEX ON computed_annual_stats USING btree (race);
CREATE INDEX ON computed_annual_stats USING btree (purpose);
CREATE INDEX ON computed_annual_stats USING btree (use_of_force);

COMMIT;
