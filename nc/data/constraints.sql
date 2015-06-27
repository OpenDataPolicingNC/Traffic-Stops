-- SQL commands to drop/create all nc_* table constraints
-- Adapted from: http://blog.hagander.net/archives/131-Automatically-dropping-and-creating-constraints.html
-- Copy psql output to import.sql

-- drop commands:
SELECT 'ALTER TABLE "'||nspname||'"."'||relname||'" DROP CONSTRAINT IF EXISTS "'||conname||'";'
 FROM pg_constraint 
 INNER JOIN pg_class ON conrelid=pg_class.oid 
 INNER JOIN pg_namespace ON pg_namespace.oid=pg_class.relnamespace 
 WHERE relname LIKE 'nc_%'
 ORDER BY CASE WHEN contype='f' THEN 0 ELSE 1 END,contype,nspname,relname,conname;

-- create commands:
SELECT 'ALTER TABLE "'||nspname||'"."'||relname||'" ADD CONSTRAINT "'||conname||'" '||pg_get_constraintdef(pg_constraint.oid)||';'
 FROM pg_constraint
 INNER JOIN pg_class ON conrelid=pg_class.oid
 INNER JOIN pg_namespace ON pg_namespace.oid=pg_class.relnamespace
 WHERE relname LIKE 'nc_%'
 ORDER BY CASE WHEN contype='f' THEN 0 ELSE 1 END DESC,contype DESC,nspname DESC,relname DESC,conname DESC;
