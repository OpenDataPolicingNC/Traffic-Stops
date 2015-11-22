-- http://www.postgresql.org/docs/current/interactive/populate.html

-- get rid of all the original data (cascades throughout app)
BEGIN;
TRUNCATE "md_stop" CASCADE;
ANALYZE;
COMMIT;

-- import stops
\set import_file :data_dir '/2013-montgomery.csv'
BEGIN;
COPY md_stop (id, location_text, agency_description, stop_date, gender, dob, race, residence_county, residence_state, registration_state, stop_reason, search_type, search_reason, disposition, outcome) FROM :'import_file' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER
    FORCE NOT NULL search_type, search_reason, disposition, residence_county, registration_state, residence_state, stop_reason, gender;
COMMIT;

-- -- populate nc_agency lookup table
BEGIN;
INSERT INTO md_agency (name) (
    SELECT DISTINCT(agency_description) from md_stop ORDER BY agency_description
);
COMMIT;

-- populate nc_stop.agency_id foreign key
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
