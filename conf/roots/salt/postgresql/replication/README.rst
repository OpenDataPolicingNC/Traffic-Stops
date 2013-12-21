PostgreSQL Streaming Replication
================================

Sample pillar (env.sls)::

    pg_replication_master: 10.10.10.2
    pg_replication_user: replicator
    pg_replication_password: ********
    max_wal_senders: 2
