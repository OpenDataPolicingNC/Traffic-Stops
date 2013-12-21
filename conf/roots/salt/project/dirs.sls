{% import 'project/_vars.sls' as vars with context %}

include:
  - project.user

root_dir:
  file.directory:
    - name: {{ vars.root_dir }}
    - user: {{ pillar['project_name'] }}
    - group: admin
    - mode: 775
    - makedirs: True
    - require:
      - user: project_user

log_dir:
  file.directory:
    - name: {{ vars.log_dir }}
    - user: {{ pillar['project_name'] }}
    - group: www-data
    - mode: 775
    - makedirs: True
    - require:
      - file: root_dir

run_dir:
  file.directory:
    - name: {{ vars.run_dir }}
    - user: {{ pillar['project_name'] }}
    - group: www-data
    - mode: 775
    - makedirs: True
    - require:
      - file: root_dir

services_dir:
  file.directory:
    - name: {{ vars.services_dir }}
    - user: {{ pillar['project_name'] }}
    - group: www-data
    - mode: 775
    - makedirs: True
    - require:
      - file: root_dir
