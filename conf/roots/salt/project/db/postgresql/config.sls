include:
  - postgresql
  - project.db.postgresql

hba_conf:
  file.managed:
    - name: /etc/postgresql/9.1/main/pg_hba.conf
    - source: salt://project/db/postgresql/pg_hba.conf
    - user: postgres
    - group: postgres
    - mode: 0640
    - template: jinja
    - require:
      - pkg: postgresql
    - watch_in:
      - service: postgresql

postgresql_conf:
  file.managed:
    - name: /etc/postgresql/9.1/main/postgresql.conf
    - source: salt://project/db/postgresql/postgresql.conf
    - user: postgres
    - group: postgres
    - mode: 0644
    - template: jinja
    - require:
      - pkg: postgresql
    - watch_in:
      - service: postgresql
