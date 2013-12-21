{% import 'project/_vars.sls' as vars with context %}

include:
  - project.app.venv
  - project.app.repo
  - project.db.pgbouncer

syncdb:
  cmd.run:
    - name: . {{ vars.venv_dir }}/bin/activate && django-admin.py syncdb --migrate --noinput --settings={{ pillar['project_name'] }}.settings.{{ pillar['environment'] }}
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
      - supervisord: supervisor_pgbouncer

# Set the domain and site name in this site's Site object to its domain
set_site:
  cmd.run:
    - name: . {{ vars.venv_dir }}/bin/activate && django-admin.py set_site --settings={{ pillar['project_name'] }}.settings.{{ pillar['environment'] }} {{ pillar['domain'] }}
    - user: {{ pillar['project_name'] }}
    - group: {{ pillar['project_name'] }}
    - env:
      - {{ pillar.get('environment_variables') }}
      - {{ pillar.get('secrets') }}
    - require:
      - cmd: syncdb
