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
              officer_id, agency_description, date, age, purpose
             ) FROM :'import_file' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER
    FORCE NOT NULL search_conducted, search_reason, seized, stop_reason, gender, ethnicity, stop_location, purpose;

-- populate md_agency lookup table

-- while the MD agency CSV *should* have all MD agencies, the raw data
-- (md_stop) could have additional agencies that aren't yet in the CSV,
-- so build the agency table from the agency values in md_stop
INSERT INTO md_agency (name, census_profile_id) (
    SELECT DISTINCT(agency_description), '' from md_stop ORDER BY agency_description
);

-- populate md_stop.agency_id foreign key
UPDATE md_stop SET agency_id = md_agency.id
FROM
   md_agency
WHERE
   md_stop.agency_description = md_agency.name;

-- update md_agency with census GEOID values from the MD agency CSV
CREATE TEMP TABLE agency_csv_table (code TEXT, name TEXT, geoid TEXT);

COPY agency_csv_table FROM :'md_csv_table' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER
    FORCE NOT NULL code, name;

UPDATE md_agency SET census_profile_id = agency_csv_table.geoid
    FROM agency_csv_table
    WHERE md_agency.name = agency_csv_table.name AND agency_csv_table.geoid IS NOT NULL;

DROP TABLE agency_csv_table;

ANALYZE;

ALTER TABLE "public"."md_stop" ADD CONSTRAINT "md_stop_pkey" PRIMARY KEY (stop_id);
ALTER TABLE "public"."md_agency" ADD CONSTRAINT "md_agency_pkey" PRIMARY KEY (id);
ALTER TABLE "public"."django_migrations" ADD CONSTRAINT "django_migrations_pkey" PRIMARY KEY (id);
ALTER TABLE "public"."md_stop" ADD CONSTRAINT "md_stop_age_check" CHECK ((age >= 0));
ALTER TABLE "public"."md_stop" ADD CONSTRAINT "md_stop_agency_id_39a3e53ab65af866_fk_md_agency_id" FOREIGN KEY (agency_id) REFERENCES md_agency(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX md_stop_169fc544 ON md_stop USING btree (agency_id);

ANALYZE;
COMMIT;
