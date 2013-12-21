include:
  - postgresql.client

pgbouncer:
  pkg:
    - installed
    - require:
      - pkg: postgresql-client
  service:
    - running
    - enable: True
