{% import 'project/_vars.sls' as vars with context %}
{% set venv_dir = vars.path_from_root('env') %}

include:
  - project.app
  - rabbitmq.project
  - supervisor

celery_conf:
  file.managed:
    - name: /etc/supervisor/conf.d/{{ vars.project }}-celery.conf
    - source: salt://project/supervisor/celery.conf
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - context:
        environment: "{{ pillar['environment'] }}"
        log_dir: "{{ vars.log_dir }}"
        root_dir: "{{ vars.root_dir }}"
        virtualenv_root: "{{ venv_dir }}"
        settings: "{{ pillar['project_name']}}.settings.{{ pillar['environment'] }}"
        project: "{{ vars.project }}"
        newrelic_config_file: "{{ vars.services_dir }}/newrelic-worker.ini"
    - require:
      - pkg: supervisor
      - file: log_dir
    - watch_in:
      - cmd: supervisor_update

celery_default_process:
  supervisord:
    - name: {{ vars.project }}:{{ vars.project }}-worker-default
    - running
    - restart: True
    - require:
      - pkg: supervisor
      - file: celery_conf

celerybeat_process:
  supervisord:
    - name: {{ vars.project }}:{{ vars.project }}-celerybeat
    - running
    - restart: True
    - require:
      - pkg: supervisor
      - file: celery_conf

extend:
  group_conf:
    file.managed:
      - context:
        project: "{{ vars.project }}"
        programs: "{{ vars.project }}-server,{{ vars.project }}-worker-default,{{ vars.project }}-celerybeat"
