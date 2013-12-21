include:
  - rabbitmq

enable-rabbitmq-management-console:
  cmd.run:
    - name: rabbitmq-plugins enable rabbitmq_management
    - unless: rabbitmq-plugins -E list | grep rabbitmq_management
    - require:
      - service: rabbitmq-server

# only restart rabbitmq if we enable management console for the first time
restart_rabbitmq:
  cmd.wait:
    - name: service rabbitmq-server restart
    - watch:
      - cmd: enable-rabbitmq-management-console
