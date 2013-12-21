{% import 'project/_vars.sls' as vars with context %}

include:
  - project.dirs
  - memcached
  - postfix
  - version-control
  - python
  - supervisor
  - project.app.venv
  - project.app.repo
  - project.app.management
  - project.app.less

group_conf:
  file.managed:
    - name: /etc/supervisor/conf.d/{{ vars.project }}-group.conf
    - source: salt://project/supervisor/group.conf
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
        programs: "{{ vars.project }}-server"
        project: "{{ vars.project }}"
    - require:
      - pkg: supervisor
      - file: log_dir
    - watch_in:
      - cmd: supervisor_update

gunicorn_conf:
  file.managed:
    - name: /etc/supervisor/conf.d/{{ vars.project }}-gunicorn.conf
    - source: salt://project/supervisor/gunicorn.conf
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
        environment: "{{ pillar['environment'] }}"
        log_dir: "{{ vars.log_dir }}"
        newrelic_config_file: "{{ vars.services_dir }}/newrelic-app.ini"
        project: "{{ vars.project }}"
        settings: "{{ pillar['project_name']}}.settings.{{ pillar['environment'] }}"
        socket: "{{ vars.server_socket }}"
        virtualenv_root: "{{ vars.venv_dir }}"
    - require:
      - pkg: supervisor
      - file: log_dir
    - watch_in:
      - cmd: supervisor_update

gunicorn_process:
  supervisord:
    - name: {{ vars.project }}:{{ vars.project }}-server
    - running
    - restart: True
    - require:
      - pkg: supervisor
      - file: gunicorn_conf
