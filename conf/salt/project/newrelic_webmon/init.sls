{% import 'project/_vars.sls' as vars with context %}

include:
  - project.dirs

newrelic_ini_app:
  file.managed:
    - name: {{ vars.services_dir }}/newrelic-app.ini
    - source: salt://project/newrelic_webmon/newrelic.ini
    - user: {{ pillar['project_name'] }}
    - group: www-data
    - mode: 440
    - template: jinja
    - context:
      log_file: "{{ vars.log_dir }}/newrelic-python-agent.log"
      newrelic_license_key: "{{ pillar['secrets']['newrelic_license_key'] }}"
      newrelic_app_name: "{{ pillar['project_name'] }} {{ pillar['environment'] }}"
    - require:
      - file: services_dir

newrelic_ini_worker:
  file.managed:
    - name: {{ vars.services_dir }}/newrelic-worker.ini
    - source: salt://project/newrelic_webmon/newrelic.ini
    - user: {{ pillar['project_name'] }}
    - group: www-data
    - mode: 440
    - template: jinja
    - context:
      log_file: "{{ vars.log_dir }}/newrelic-python-agent.log"
      newrelic_license_key: "{{ pillar['secrets']['newrelic_license_key'] }}"
      newrelic_app_name: "{{ pillar['project_name'] }} {{ pillar['environment'] }}"
    - require:
      - file: services_dir
