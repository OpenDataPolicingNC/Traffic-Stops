include:
  - postgresql
  - locale.utf8

pg_replication_user:
  postgres_user.present:
    - name: {{ pillar['pg_replication_user'] }}
    - password: {{ pillar['pg_replication_password'] }}
    - replication: True
    - require:
      - service: postgresql
