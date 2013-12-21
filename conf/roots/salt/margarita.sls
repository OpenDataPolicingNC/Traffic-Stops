git-install:
  pkg.installed:
    - name: git-core

project_repo:
  git.latest:
    - name: https://github.com/caktus/margarita.git
    - rev: master
    - target: /srv/common
    - user: root
    - require:
      - pkg: git-install
