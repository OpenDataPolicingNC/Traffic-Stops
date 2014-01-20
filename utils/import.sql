-- http://www.postgresql.org/docs/current/interactive/populate.html

-- get rid of all the indexes
BEGIN;
DROP INDEX IF EXISTS "stops_person_stop_id";
DROP INDEX IF EXISTS "stops_search_stop_id";
DROP INDEX IF EXISTS "stops_search_person_id";
DROP INDEX IF EXISTS "stops_contraband_search_id";
DROP INDEX IF EXISTS "stops_contraband_person_id";
DROP INDEX IF EXISTS "stops_contraband_stop_id";
DROP INDEX IF EXISTS "stops_searchbasis_search_id";
DROP INDEX IF EXISTS "stops_searchbasis_person_id";
DROP INDEX IF EXISTS "stops_searchbasis_stop_id";
COMMIT;

-- get rid of all the original data (cascades throughout app)
BEGIN;
TRUNCATE "stops_stop" CASCADE;
ANALYZE;
COMMIT;

-- import stops
BEGIN;
COPY stops_stop FROM '/home/shapiromatron/dev/raw-data/STOP.csv' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER
    FORCE NOT NULL officer_id, stop_city, stop_location;
COMMIT;

-- import persons
BEGIN;
COPY stops_person FROM '/home/shapiromatron/dev/raw-data/PERSON.csv' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER
    FORCE NOT NULL ethnicity, gender, race; --required; might be an issue later on...
COMMIT;

-- import searches
BEGIN;
COPY stops_search FROM '/home/shapiromatron/dev/raw-data/SEARCH.csv' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER;
COMMIT;

-- import contraband
BEGIN;
COPY stops_contraband FROM '/home/shapiromatron/dev/raw-data/CONTRABAND.csv' WITH
    DELIMITER ','
    CSV HEADER;
COMMIT;

-- import search-basis
BEGIN;
COPY stops_searchbasis FROM '/home/shapiromatron/dev/raw-data/SEARCHBASIS.csv' WITH
    DELIMITER ','
    CSV HEADER;
COMMIT;

BEGIN;
ANALYZE;
COMMIT;

-- rebuild indexes
BEGIN;
CREATE INDEX "stops_person_stop_id" ON "stops_person" ("stop_id");
CREATE INDEX "stops_search_stop_id" ON "stops_search" ("stop_id");
CREATE INDEX "stops_search_person_id" ON "stops_search" ("person_id");
CREATE INDEX "stops_contraband_search_id" ON "stops_contraband" ("search_id");
CREATE INDEX "stops_contraband_person_id" ON "stops_contraband" ("person_id");
CREATE INDEX "stops_contraband_stop_id" ON "stops_contraband" ("stop_id");
CREATE INDEX "stops_searchbasis_search_id" ON "stops_searchbasis" ("search_id");
CREATE INDEX "stops_searchbasis_person_id" ON "stops_searchbasis" ("person_id");
CREATE INDEX "stops_searchbasis_stop_id" ON "stops_searchbasis" ("stop_id");
COMMIT;

