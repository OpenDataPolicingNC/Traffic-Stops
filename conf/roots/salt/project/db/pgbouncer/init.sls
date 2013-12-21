{% import 'project/_vars.sls' as vars with context %}

include:
  - project.dirs
  - supervisor
  - pgbouncer
  - project.db.postgresql
  - project.db.postgresql.config

userlist_txt:
  file.managed:
    - name: {{ vars.services_dir}}/userlist.txt
    - source: salt://project/db/pgbouncer/userlist.txt
    - user: {{ pillar['project_name'] }}
    - group: {{ pillar['project_name'] }}
    - mode: 640
    - template: jinja
    - require:
      - pkg: pgbouncer
      - file: services_dir
      - postgres_database: database-{{ pillar['project_name'] }}

pgbouncer_ini:
  file.managed:
    - name: {{ vars.services_dir}}/pgbouncer.ini
    - source: salt://project/db/pgbouncer/pgbouncer.ini
    - user: {{ pillar['project_name'] }}
    - group: {{ pillar['project_name'] }}
    - mode: 640
    - template: jinja
    - context:
        log_dir: "{{ vars.log_dir }}"
        services_dir: "{{ vars.services_dir }}"
        run_dir: "{{ vars.run_dir }}"
    - require:
      - pkg: pgbouncer
      - file: userlist_txt
      - postgres_database: database-{{ pillar['project_name'] }}

touch_pgbouncer_log:
  file.touch:
    - name: {{ vars.log_dir }}/pgbouncer.log
    - require:
      - file: log_dir

chown_pgbouncer_log:
  cmd.run:
    - name: "chown {{ pillar['project_name'] }}:{{ pillar['project_name'] }} {{ vars.log_dir }}/pgbouncer.log"
    - user: root
    - group: root
    - require:
      - file: touch_pgbouncer_log

supervisor_pgbouncer_conf:
  file.managed:
    - name: /etc/supervisor/conf.d/{{ vars.project }}-pgbouncer.conf
    - source: salt://project/supervisor/pgbouncer.conf
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
        log_dir: "{{ vars.log_dir }}"
        project: "{{ vars.project }}"
        services_dir: "{{ vars.services_dir }}"
    - require:
      - pkg: pgbouncer
      - pkg: supervisor
      - file: log_dir
      - file: pgbouncer_ini
      - file: userlist_txt
      - cmd: chown_pgbouncer_log

supervisor_pgbouncer:
  supervisord.running:
    - name: {{ vars.project }}-pgbouncer
    - update: True
    - restart: True
    - require:
      - pkg: supervisor
      - file: supervisor_pgbouncer_conf
      - postgres_database: database-{{ pillar['project_name'] }}
    - watch:
      - file: supervisor_pgbouncer_conf
