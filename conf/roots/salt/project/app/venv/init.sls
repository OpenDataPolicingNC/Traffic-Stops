{% import 'project/_vars.sls' as vars with context %}
{% set venv_dir = vars.path_from_root('env') %}

include:
  - project.dirs
  - project.app.repo
  - postgresql.dev
  - python

venv:
  virtualenv.managed:
    - name: {{ venv_dir }}
    - system_site_packages: False
    - distribute: True
    - requirements: {{ vars.build_path(vars.source_dir, 'requirements/production.txt') }}
    - user: {{ pillar['project_name'] }}
    - no_chown: True
    - require:
      - pip: virtualenv
      - file: root_dir
      - git: project_repo
      - pkg: postgresql_dev
      - pkg: python-headers

venv_dir:
  file.directory:
    - name: {{ venv_dir }}
    - user: {{ pillar['project_name'] }}
    - group: {{ pillar['project_name'] }}
    - recurse:
      - user
      - group
    - require:
      - virtualenv: venv

project_path:
  file.managed:
    - source: salt://project/app/venv/project.pth
    - name: {{ vars.build_path(venv_dir, 'lib/python2.7/site-packages/project.pth') }}
    - user: {{ pillar['project_name'] }}
    - group: {{ pillar['project_name'] }}
    - template: jinja
    - context:
      source_dir: {{ vars.source_dir }}

secrets:
  file.managed:
    - name: {{ vars.build_path(venv_dir, "bin/secrets") }}
    - source: salt://project/app/venv/env_secrets.jinja2
    - user: {{ pillar['project_name'] }}
    - group: {{ pillar['project_name'] }}
    - template: jinja
    - context:
      settings: "{{ pillar['project_name']}}.settings.{{ pillar['environment'] }}"
