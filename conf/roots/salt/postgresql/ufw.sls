include:
  - ufw
  - postgresql

allow_postgres_conns:
  ufw.allow:
    - name: '5432'
    - enabled: true
    - require:
      - pkg: ufw
