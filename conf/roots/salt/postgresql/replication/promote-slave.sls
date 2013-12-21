{% set postgresql_data_dir = "/var/lib/postgresql/9.1/main/" %}

pg-promote-slave:
  cmd.run:
    - name: /usr/lib/postgresql/9.1/bin/pg_ctl -D {{ postgresql_data_dir }} promote
    - user: postgres
    - unless: /usr/lib/postgresql/9.1/bin/pg_controldata {{ postgresql_data_dir }} | grep cluster | grep production
