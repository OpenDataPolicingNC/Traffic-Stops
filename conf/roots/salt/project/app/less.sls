node_ppa:
  pkgrepo.managed:
    - ppa: chris-lea/node.js

nodejs:
  pkg.installed:
    - require:
      - pkgrepo: node_ppa
    - refresh: True

less:
  cmd.run:
    - name: npm install less@1.5.0 -g
    - user: root
    - unless: which lessc
    - require:
      - pkg: nodejs
