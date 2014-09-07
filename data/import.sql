-- http://www.postgresql.org/docs/current/interactive/populate.html

-- get rid of all the indexes
-- BEGIN;
-- DROP INDEX IF EXISTS "stops_person_stop_id";
-- DROP INDEX IF EXISTS "stops_search_stop_id";
-- DROP INDEX IF EXISTS "stops_search_person_id";
-- DROP INDEX IF EXISTS "stops_contraband_search_id";
-- DROP INDEX IF EXISTS "stops_contraband_person_id";
-- DROP INDEX IF EXISTS "stops_contraband_stop_id";
-- DROP INDEX IF EXISTS "stops_searchbasis_search_id";
-- DROP INDEX IF EXISTS "stops_searchbasis_person_id";
-- DROP INDEX IF EXISTS "stops_searchbasis_stop_id";
-- COMMIT;

-- get rid of all the original data (cascades throughout app)
BEGIN;
TRUNCATE "stops_stop" CASCADE;
ANALYZE;
COMMIT;

-- import stops
\set import_file :data_dir '/STOP.csv'
BEGIN;
COPY stops_stop FROM :'import_file' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER
    FORCE NOT NULL officer_id, stop_city, stop_location;
COMMIT;

-- import persons
\set import_file :data_dir '/PERSON.csv'
BEGIN;
COPY stops_person (person_id, stop_id, type, age, gender, ethnicity, race) FROM :'import_file' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER
    FORCE NOT NULL ethnicity, gender, race; --required; might be an issue later on...
COMMIT;

-- import searches
\set import_file :data_dir '/SEARCH.csv'
BEGIN;
COPY stops_search (search_id, stop_id, person_id, type, vehicle_search, driver_search, passenger_search, property_search, vehicle_siezed, personal_property_siezed, other_property_sized) FROM :'import_file' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER;
COMMIT;

-- import contraband
\set import_file :data_dir '/CONTRABAND.csv'
BEGIN;
COPY stops_contraband (contraband_id, search_id, person_id, stop_id, ounces, pounds, pints, gallons, dosages, grams, kilos, money, weapons, dollar_amount) FROM :'import_file' WITH
    DELIMITER ','
    CSV HEADER;
COMMIT;

-- import search-basis
BEGIN;
\set import_file :data_dir '/SEARCHBASIS.csv'
COPY stops_searchbasis (search_basis_id, search_id, person_id, stop_id, basis) FROM :'import_file' WITH
    DELIMITER ','
    CSV HEADER;
COMMIT;

BEGIN;
ANALYZE;
COMMIT;

-- rebuild indexes
-- BEGIN;
-- CREATE INDEX "stops_person_stop_id" ON "stops_person" ("stop_id");
-- CREATE INDEX "stops_search_stop_id" ON "stops_search" ("stop_id");
-- CREATE INDEX "stops_search_person_id" ON "stops_search" ("person_id");
-- CREATE INDEX "stops_contraband_search_id" ON "stops_contraband" ("search_id");
-- CREATE INDEX "stops_contraband_person_id" ON "stops_contraband" ("person_id");
-- CREATE INDEX "stops_contraband_stop_id" ON "stops_contraband" ("stop_id");
-- CREATE INDEX "stops_searchbasis_search_id" ON "stops_searchbasis" ("search_id");
-- CREATE INDEX "stops_searchbasis_person_id" ON "stops_searchbasis" ("person_id");
-- CREATE INDEX "stops_searchbasis_stop_id" ON "stops_searchbasis" ("stop_id");
-- COMMIT;
