{% set version=pillar.get("postgresql_version", "9.3") %}

include:
  - locale.utf8

postgresql-apt-repo:
  pkgrepo.managed:
    - name: 'deb http://apt.postgresql.org/pub/repos/apt/ {{ grains['oscodename'] }}-pgdg main'
    - file: /etc/apt/sources.list.d/pgdg.list
    - key_url: https://www.postgresql.org/media/keys/ACCC4CF8.asc

db-packages:
  pkg:
    - installed
    - names:
      - postgresql-{{ version }}
      - libpq-dev
    - require:
      - pkgrepo: postgresql-apt-repo

postgresql:
  pkg:
    - installed
  service:
    - running
    - enable: True

{% if 'postgis' in pillar['postgresql_extensions'] %}
postgis-packages:
  pkg:
    - installed
    - names:
      - postgresql-{{ version }}-postgis-2.1
    - require:
      - pkg: db-packages
{% endif %}
