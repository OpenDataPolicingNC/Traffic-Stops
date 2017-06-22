{% import 'project/_vars.sls' as vars with context %}

{% set pg_version = salt['pillar.get']('postgres_version', '9.3') %}

include:
  - postgresql
  - ufw

user-etl:
  postgres_user.present:
    - name: etl
    - superuser: True
    - encrypted: True
    - require:
      - service: postgresql

user-{{ pillar['project_name'] }}:
  postgres_user.present:
    - name: {{ pillar['project_name'] }}_{{ pillar['environment'] }}
    - createdb: False
    - createuser: False
    - superuser: False
    - password: {{ pillar.get('secrets', {}).get('DB_PASSWORD', '') }}
    - encrypted: True
    - require:
      - service: postgresql

database-{{ pillar['project_name'] }}:
  postgres_database.present:
    - name: {{ pillar['project_name'] }}_{{ pillar['environment'] }}
    - owner: {{ pillar['project_name'] }}_{{ pillar['environment'] }}
    - template: template0
    - encoding: UTF8
    - lc_collate: en_US.UTF-8
    - lc_ctype: en_US.UTF-8
    - require:
      - postgres_user: user-{{ pillar['project_name'] }}
      - file: hba_conf
      - file: postgresql_conf

### State DBs ###
{% for instance in salt['pillar.get']('instances') %}
database-{{ pillar['project_name'] }}-{{ instance }}:
  postgres_database.present:
    - name: {{ pillar['project_name'] }}_{{ instance }}_{{ pillar['environment'] }}
    - owner: {{ pillar['project_name'] }}_{{ pillar['environment'] }}
    - template: template0
    - encoding: UTF8
    - locale: en_US.UTF-8
    - lc_collate: en_US.UTF-8
    - lc_ctype: en_US.UTF-8
    - require:
      - postgres_user: user-{{ pillar['project_name'] }}
      - file: hba_conf
      - file: postgresql_conf
    - require_in:
      - postgres_database: database-{{ pillar['project_name'] }}
{% endfor %}

hba_conf:
  file.managed:
    - name: /etc/postgresql/{{ pg_version }}/main/pg_hba.conf
    - source: salt://project/db/pg_hba.conf
    - user: postgres
    - group: postgres
    - mode: 0640
    - template: jinja
    - context:
        version: "{{ pg_version }}"
        servers:
{%- for host, ifaces in vars.app_minions.items() %}
          - {{ vars.get_primary_ip(host, ifaces) }}
{% endfor %}
    - require:
      - pkg: postgresql
    - watch_in:
      - service: postgresql

postgresql_conf:
  file.managed:
    - name: /etc/postgresql/{{ pg_version }}/main/postgresql.conf
    - source: salt://project/db/postgresql.conf
    - user: postgres
    - group: postgres
    - mode: 0644
    - template: jinja
    - context:
        version: "{{ pg_version }}"
    - require:
      - pkg: postgresql
    - watch_in:
      - service: postgresql

{% for host, ifaces in vars.app_minions.items() %}
db_allow-{{ vars.get_primary_ip(host, ifaces) }}:
  ufw.allow:
    - name: '5432'
    - enabled: true
    - from: {{ vars.get_primary_ip(host, ifaces) }}
    - require:
      - pkg: ufw
{% endfor %}

{% for extension in pillar.get('postgres_extensions', []) %}
create-{{ extension }}-extension:
  cmd.run:
    - name: psql -U postgres {{ pillar['project_name'] }}_{{ pillar['environment'] }} -c "CREATE EXTENSION postgis;"
    - unless: psql -U postgres {{ pillar['project_name'] }}_{{ pillar['environment'] }} -c "\dx+" | grep postgis
    - user: postgres
    - require:
      - pkg: postgis-packages
      - postgres_database: database-{{ pillar['project_name'] }}
    - require_in:
      - virtualenv: venv

{% for instance in salt['pillar.get']('instances') %}
create-{{ extension }}-{{ instance }}-extension:
  cmd.run:
    - name: psql -U postgres {{ pillar['project_name'] }}_{{ instance }}_{{ pillar['environment'] }} -c "CREATE EXTENSION postgis;"
    - unless: psql -U postgres {{ pillar['project_name'] }}_{{ pillar['environment'] }} -c "\dx+" | grep postgis
    - user: postgres
    - require:
      - pkg: postgis-packages
      - postgres_database: database-{{ pillar['project_name'] }}
    - require_in:
      - virtualenv: venv
{% endfor %}

{% endfor %}
