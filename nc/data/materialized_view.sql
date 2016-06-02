-- psql -f materialized_view.sql traffic_stops_nc

BEGIN;

DROP MATERIALIZED VIEW IF EXISTS computed_annual_stats;

CREATE MATERIALIZED VIEW computed_annual_stats
AS
SELECT s.agency_id,
       EXTRACT(YEAR FROM s.date) AS year,
       s.officer_id,
       p.race,
       p.ethnicity,
       s.purpose,
       s.engage_force AS use_of_force,
       COUNT(p.person_id) AS stops,
       COUNT(se.search_id) AS searches
FROM nc_person p
JOIN nc_stop s ON p.stop_id = s.stop_id
LEFT OUTER JOIN nc_search se ON s.stop_id = se.stop_id
WHERE p.type='D'
  -- AND s.agency_id = 1021
GROUP BY s.agency_id,
         year,
         s.officer_id,
         p.race,
         p.ethnicity,
         use_of_force,
         s.purpose
-- ORDER BY year ASC,
--          s.officer_id,
--          s.purpose ASC,
--          p.race DESC
WITH DATA;

CREATE INDEX ON computed_annual_stats USING btree (agency_id);
CREATE INDEX ON computed_annual_stats USING btree (year);
CREATE INDEX ON computed_annual_stats USING btree (officer_id);
CREATE INDEX ON computed_annual_stats USING btree (race);
CREATE INDEX ON computed_annual_stats USING btree (ethnicity);
CREATE INDEX ON computed_annual_stats USING btree (purpose);
CREATE INDEX ON computed_annual_stats USING btree (use_of_force);

COMMIT;
