{% import 'project/_vars.sls' as vars with context %}
{% set identity = vars.build_path(vars.services_dir, 'github-deploy-key') %}

include:
  - project.dirs
  - version-control
  - sshd.github

project_repo_identity:
  file.managed:
    - name: {{ identity }}
    - source: salt://project/app/repo/private-key
    - user: {{ pillar['project_name'] }}
    - group: {{ pillar['project_name'] }}
    - mode: 600
    - template: jinja
    - require:
      - file: services_dir

project_repo:
  git.latest:
    - name: "{{ salt['pillar.get']('repo:url') }}"
    - rev: "{{ salt['pillar.get']('repo:branch', 'master') }}"
    - target: {{ vars.source_dir }}
    - user: {{ pillar['project_name'] }}
    - identity: {{ identity }}
    - require:
      - file: root_dir
      - pkg: git-core
      - file: project_repo_identity
      - ssh_known_hosts: github.com
