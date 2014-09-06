{% if 'postgis' in pillar['postgres_extensions'] %}
nginx_repo:
  pkgrepo.managed:
    - name: 'deb http://apt.postgresql.org/pub/repos/apt/ {{ grains['oscodename'] }}-pgdg main'
    - file: /etc/apt/sources.list.d/pgdg.list
    - key_url: https://www.postgresql.org/media/keys/ACCC4CF8.asc
    - require_in:
        - pkg: nginx
# ubuntugis:
#   pkgrepo.managed:
#     - humanname: UbuntuGIS PPA
#     - ppa: ubuntugis/ppa

# postgis-packages:
#   pkg:
#     - installed
#     - names:
#       - postgresql-9.1-postgis-2.0
#     - require:
#       - pkgrepo: ubuntugis
#       - pkg: db-packages
#     - require_in:
#       - virtualenv: venv
{% endif %}

# {% for extension in pillar['postgres_extensions'] %}
# create-{{ extension }}-extension:
#   cmd.run:
#     - name: psql -U postgres {{ pillar['project_name'] }}_{{ pillar['environment'] }} -c "CREATE EXTENSION postgis;"
#     - unless: psql -U postgres {{ pillar['project_name'] }}_{{ pillar['environment'] }} -c "\dx+" | grep postgis
#     - user: postgres
#     - require:
#       - pkg: postgis-packages
#       - postgres_database: database-{{ pillar['project_name'] }}
#     - require_in:
#       - virtualenv: venv
# {% endfor %}
