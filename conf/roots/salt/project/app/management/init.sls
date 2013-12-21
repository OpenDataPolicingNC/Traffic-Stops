{% import 'project/_vars.sls' as vars with context %}

include:
  - project.app.venv
  - project.app.repo
  - project.db.pgbouncer

collectstatic:
  cmd.run:
    - name: . {{ vars.venv_dir }}/bin/activate && django-admin.py collectstatic --noinput --settings={{ pillar['project_name'] }}.settings.{{ pillar['environment'] }}
    - user: {{ pillar['project_name'] }}
    - group: {{ pillar['project_name'] }}
    - env:
      - {{ pillar.get('environment_variables') }}
      - {{ pillar.get('secrets') }}
    - require:
      - git: project_repo
      - virtualenv: venv
      - file: project_path
      - file: log_dir
