import logging


logger = logging.getLogger(__name__)


def get_add_constraints_and_indexes(cursor):
    """
    Inspect cursor's current database constraints and indexes and
    and return SQL statements to recreate the constraints and indexes.
    """
    sql = get_sql_statements(cursor, SELECT_ADD_CONSTRAINTS_SQL)
    sql += get_sql_statements(cursor, SELECT_ADD_INDEXES_SQL)
    return sql


def drop_constraints_and_indexes(cursor):
    """Inspect and DROP cursor's current database constraints and indexes"""
    # inspect table constraints so we can toggle them off during import
    sql = get_sql_statements(cursor, SELECT_DROP_CONSTRAINTS_SQL)
    sql += get_sql_statements(cursor, SELECT_DROP_INDEXES_SQL)
    # drop constraints to speed up import
    if sql:
        logger.info("Dropping table constraints and indexes")
        logger.info(sql)
        cursor.execute(sql)


def get_sql_statements(cursor, select_sql):
    """
    Simple wrapper function used to execute a SQL query that returns a
    list of SQL commands to be run later.
    """
    # Explicitly pass None for params to avoid different behavior when
    # running through Django Debug Toolbar (it defaults params to (),
    # Django expects None for no params).
    cursor.execute(select_sql, params=None)
    sql = ''
    for row in cursor.fetchall():
        sql += '{}\n'.format(row[0])
    return sql


# SQL commands to drop all nc_* table constraints and indexes
# Adapted from: http://blog.hagander.net/archives/131-Automatically-dropping-and-creating-constraints.html  # noqa


SELECT_DROP_CONSTRAINTS_SQL = """
SELECT 'ALTER TABLE "'||nspname||'"."'||relname||'" DROP CONSTRAINT IF EXISTS "'||conname||'";'
FROM pg_constraint
INNER JOIN pg_class ON conrelid=pg_class.oid
INNER JOIN pg_namespace ON pg_namespace.oid=pg_class.relnamespace
WHERE relname NOT LIKE 'pg_%'
ORDER BY CASE WHEN contype='f' THEN 0 ELSE 1 END,contype,nspname,relname,conname;
"""  # noqa

SELECT_DROP_INDEXES_SQL = """
SELECT 'DROP INDEX "'||nspname||'"."'||relname||'" RESTRICT;'
FROM pg_index
INNER JOIN pg_class ON indexrelid=pg_class.oid
INNER JOIN pg_namespace ON pg_namespace.oid=pg_class.relnamespace
WHERE indisprimary=FALSE
      AND indisvalid=TRUE
      AND nspname NOT LIKE 'pg_%'
ORDER BY nspname, relname;
"""  # noqa

SELECT_ADD_CONSTRAINTS_SQL = """
SELECT 'ALTER TABLE "'||nspname||'"."'||relname||'" ADD CONSTRAINT "'||conname||'" '||pg_get_constraintdef(pg_constraint.oid)||';'
FROM pg_constraint
INNER JOIN pg_class ON conrelid=pg_class.oid
INNER JOIN pg_namespace ON pg_namespace.oid=pg_class.relnamespace
WHERE relname LIKE 'nc_%'
ORDER BY CASE WHEN contype='f' THEN 0 ELSE 1 END DESC,contype DESC,nspname DESC,relname DESC,conname DESC;
"""  # noqa

SELECT_ADD_INDEXES_SQL = """
SELECT pg_get_indexdef(pg_index.indexrelid)||';'
FROM pg_index
INNER JOIN pg_class ON indexrelid=pg_class.oid
INNER JOIN pg_namespace ON pg_namespace.oid=pg_class.relnamespace
WHERE indisprimary=FALSE
      AND indisvalid=TRUE
      AND nspname NOT LIKE 'pg_%'
ORDER BY nspname, relname;
"""  # noqa
