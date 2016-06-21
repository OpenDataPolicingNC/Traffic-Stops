-- http://www.postgresql.org/docs/current/interactive/populate.html

\set ON_ERROR_STOP 1

-- get rid of all the original data (cascades throughout app)
BEGIN;
TRUNCATE "md_stop" CASCADE;
ANALYZE;
COMMIT;

-- import stops
\set import_file :data_file
BEGIN;
COPY md_stop (stop_id, date, stop_date_text, stop_time_text,
              location_text, duration_text, stop_reason, search_conducted,
              search_reason, what_searched, seized, stop_outcome,
              crime_charged, registration_state, gender,
              date_of_birth_text, residence_state, county, ethnicity,
              officer_id, agency_description
             ) FROM :'import_file' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER
    FORCE NOT NULL search_conducted, search_reason, seized, county, registration_state, residence_state, stop_reason, gender, ethnicity, stop_outcome, location_text;
COMMIT;

-- -- populate md_agency lookup table
BEGIN;
INSERT INTO md_agency (name) (
    SELECT DISTINCT(agency_description) from md_stop ORDER BY agency_description
);
COMMIT;

-- populate md_stop.agency_id foreign key
BEGIN;
UPDATE md_stop SET agency_id = md_agency.id
FROM
   md_agency
WHERE
   md_stop.agency_description = md_agency.name;
COMMIT;

BEGIN;
ANALYZE;
COMMIT;
