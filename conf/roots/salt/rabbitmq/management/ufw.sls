include:
  - ufw

allow_rabbitmq_conns:
  ufw.allow:
    - name: '15672'
    - enabled: true
    - require:
      - pkg: ufw
