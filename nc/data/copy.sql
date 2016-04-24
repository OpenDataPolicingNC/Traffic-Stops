-- http://www.postgresql.org/docs/current/interactive/populate.html

-- get rid of all the original data (cascades throughout app)
BEGIN;
TRUNCATE "nc_stop" CASCADE;
ANALYZE;
COMMIT;

SET ROLE :owner;

-- import stops
\set import_file :data_dir '/STOP.csv'
BEGIN;
COPY nc_stop (stop_id, agency_description, date, purpose, action, driver_arrest, passenger_arrest, encounter_force, engage_force, officer_injury, driver_injury, passenger_injury, officer_id, stop_location, stop_city) FROM :'import_file' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER
    FORCE NOT NULL officer_id, stop_city, stop_location;
COMMIT;

-- import persons
\set import_file :data_dir '/PERSON.csv'
BEGIN;
COPY nc_person (person_id, stop_id, type, age, gender, ethnicity, race) FROM :'import_file' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER
    FORCE NOT NULL ethnicity, gender, race; --required; might be an issue later on...
COMMIT;

-- import searches
\set import_file :data_dir '/SEARCH.csv'
BEGIN;
COPY nc_search (search_id, stop_id, person_id, type, vehicle_search, driver_search, passenger_search, property_search, vehicle_siezed, personal_property_siezed, other_property_sized) FROM :'import_file' WITH
    DELIMITER ','
    NULL AS ''
    CSV HEADER;
COMMIT;

-- import contraband
\set import_file :data_dir '/CONTRABAND.csv'
BEGIN;
COPY nc_contraband (contraband_id, search_id, person_id, stop_id, ounces, pounds, pints, gallons, dosages, grams, kilos, money, weapons, dollar_amount) FROM :'import_file' WITH
    DELIMITER ','
    CSV HEADER;
COMMIT;

-- import search-basis
BEGIN;
\set import_file :data_dir '/SEARCHBASIS.csv'
COPY nc_searchbasis (search_basis_id, search_id, person_id, stop_id, basis) FROM :'import_file' WITH
    DELIMITER ','
    CSV HEADER;
COMMIT;


-- -- populate nc_agency lookup table
BEGIN;
INSERT INTO nc_agency (name) (
    SELECT DISTINCT(agency_description) from nc_stop ORDER BY agency_description
);
COMMIT;

-- populate nc_stop.agency_id foreign key
BEGIN;
UPDATE nc_stop SET agency_id = nc_agency.id
FROM
   nc_agency
WHERE
   nc_stop.agency_description = nc_agency.name;
COMMIT;

BEGIN;
CREATE INDEX ON nc_stop (purpose);
CREATE INDEX ON nc_stop (date);
CREATE INDEX ON nc_person (type);
CREATE INDEX ON nc_person (race);
CREATE INDEX ON nc_person (ethnicity);
COMMIT;

BEGIN;
ANALYZE;
COMMIT;
