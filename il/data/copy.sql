-- http://www.postgresql.org/docs/current/interactive/populate.html

\set ON_ERROR_STOP true

BEGIN;

SET TIMEZONE=:'il_time_zone';

-- get rid of all the original data (cascades throughout app)
TRUNCATE "il_stop" RESTART IDENTITY CASCADE;
TRUNCATE "il_agency" RESTART IDENTITY CASCADE;

-- import stops
\set import_file :data_file
COPY il_stop (stop_id, gender, ethnicity, search_conducted, seized,
              year, purpose, agency_description
             ) FROM :'import_file' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER
    FORCE NOT NULL search_conducted, seized, gender, ethnicity, purpose;

-- populate il_agency lookup table

-- while the IL agency CSV *should* have all IL agencies, the raw data
-- (il_stop) could have additional agencies that aren't yet in the CSV,
-- so build the agency table from the agency values in il_stop
INSERT INTO il_agency (name, census_profile_id) (
    SELECT DISTINCT(agency_description), '' from il_stop ORDER BY agency_description
);

-- populate il_stop.agency_id foreign key
UPDATE il_stop SET agency_id = il_agency.id
FROM
   il_agency
WHERE
   il_stop.agency_description = il_agency.name;

-- update il_agency with census GEOID values from the IL agency CSV
CREATE TEMP TABLE agency_csv_table (code TEXT, name TEXT, geoid TEXT);

COPY agency_csv_table FROM :'il_csv_table' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER
    FORCE NOT NULL code, name;

UPDATE il_agency SET census_profile_id = agency_csv_table.geoid
    FROM agency_csv_table
    WHERE il_agency.name = agency_csv_table.name AND agency_csv_table.geoid IS NOT NULL;

DROP TABLE agency_csv_table;

ANALYZE;

ALTER TABLE "public"."il_stop" ADD CONSTRAINT "il_stop_pkey" PRIMARY KEY (stop_id);
ALTER TABLE "public"."il_agency" ADD CONSTRAINT "il_agency_pkey" PRIMARY KEY (id);
ALTER TABLE "public"."django_migrations" ADD CONSTRAINT "django_migrations_pkey" PRIMARY KEY (id);
ALTER TABLE "public"."il_stop" ADD CONSTRAINT "il_stop_year_13b4a60c0ac76bed_check" CHECK ((year >= 0));
ALTER TABLE "public"."il_stop" ADD CONSTRAINT "il_stop_purpose_check" CHECK ((purpose >= 0));
ALTER TABLE "public"."il_stop" ADD CONSTRAINT "il_stop_agency_id_7609bd7ab1150409_fk_il_agency_id" FOREIGN KEY (agency_id) REFERENCES il_agency(id) DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX il_stop_169fc544 ON il_stop USING btree (agency_id);

ANALYZE;
COMMIT;
