-- http://www.postgresql.org/docs/current/interactive/populate.html

\set ON_ERROR_STOP true

BEGIN;

-- get rid of all the original data (cascades throughout app)
TRUNCATE "md_stop" RESTART IDENTITY CASCADE;
TRUNCATE "md_agency" RESTART IDENTITY CASCADE;

-- import stops
\set import_file :data_file
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

-- -- populate md_agency lookup table
INSERT INTO md_agency (name) (
    SELECT DISTINCT(agency_description) from md_stop ORDER BY agency_description
);

-- populate md_stop.agency_id foreign key
UPDATE md_stop SET agency_id = md_agency.id
FROM
   md_agency
WHERE
   md_stop.agency_description = md_agency.name;

ANALYZE;

CREATE INDEX md_stop_169fc544 ON md_stop USING btree (agency_id);

ANALYZE;
COMMIT;
