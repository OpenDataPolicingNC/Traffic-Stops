base:
  "*":
    - devs
    - project
  'G@environment:staging':
    - match: compound
    - staging.env
    - staging.secrets
  'G@environment:production':
    - match: compound
    - production.env
    - production.secrets
  'G@environment:vagrant':
    - match: compound
    - vagrant.env
    - vagrant.secrets
