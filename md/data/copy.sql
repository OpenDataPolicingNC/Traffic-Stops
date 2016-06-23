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
COPY md_stop (stop_id, stop_date_text, stop_time_text,
              stop_location, duration_text, stop_reason, search_conducted,
              search_reason, seized, gender,
              date_of_birth_text, ethnicity,
              officer_id, agency_description, date, age
             ) FROM :'import_file' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER
    FORCE NOT NULL search_conducted, search_reason, seized, stop_reason, gender, ethnicity, stop_location;
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
