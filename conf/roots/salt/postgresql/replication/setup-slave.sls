# adapted from:
# http://www.rassoc.com/gregr/weblog/2013/02/16/zero-to-postgresql-streaming-replication-in-10-mins/
{% set postgresql_data_dir = "/var/lib/postgresql/9.1/main/" %}

pg-pass-file:
  file.managed:
    - name: /var/lib/postgresql/.pgpass
    - source: salt://postgresql/replication/pgpass
    - user: postgres
    - group: postgres
    - mode: 600
    - template: jinja

pg-stop:
  cmd.run:
    - name: service postgresql stop
    - prereq:
      - cmd: pg-delete-old-cluster

pg-delete-old-cluster:
  cmd.run:
    - name: rm -rf {{ postgresql_data_dir }}
    - user: postgres
    - onlyif: test -d {{ postgresql_data_dir }}

pg-run-basebackup:
  cmd.run:
    - name: pg_basebackup -h {{ pillar['pg_replication_master'] }} -D {{ postgresql_data_dir }} -U {{ pillar['pg_replication_user'] }} -v -w
    - user: postgres
    - require:
      - file: pg-pass-file
      - cmd: pg-delete-old-cluster

pg-crt-symlink:
  file.symlink:
    - target: /etc/ssl/certs/ssl-cert-snakeoil.pem
    - name: {{ postgresql_data_dir }}server.crt
    - user: postgres
    - group: postgres
    - mode: 777
    - require:
      - cmd: pg-run-basebackup

pg-key-symlink:
  file.symlink:
    - target: /etc/ssl/private/ssl-cert-snakeoil.key
    - name: {{ postgresql_data_dir }}server.key
    - user: postgres
    - group: postgres
    - mode: 777
    - require:
      - cmd: pg-run-basebackup

pg-recovery-conf:
  file.managed:
    - name: {{ postgresql_data_dir }}recovery.conf
    - source: salt://postgresql/replication/recovery.conf
    - user: postgres
    - group: postgres
    - mode: 600
    - template: jinja
    - require:
      - file: pg-crt-symlink
      - file: pg-key-symlink

pg-start:
  cmd.run:
    - name: service postgresql start
    - require:
      - file: pg-recovery-conf
