{% import 'project/_vars.sls' as vars with context %}

include:
  - project.web.app

### State DBs ###
{% for instance in salt['pillar.get']('instances') %}
{% set db_alias = pillar['project_name'] + '_' + instance %}
migrate-{{ instance }}:
  cmd.run:
    - name: "{{ vars.path_from_root('manage.sh') }} migrate --database={{ db_alias }} --noinput"
    - user: {{ pillar['project_name'] }}
    - group: {{ pillar['project_name'] }}
    - require:
      - cmd: migrate
    - order: last
{% endfor %}
