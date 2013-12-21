include:
  - project.queue.management-admin

rabbit_policy:
  cmd.run:
    - name: rabbitmqctl set_policy -p {{ pillar['project_name'] }}_{{ pillar['environment'] }} ha-all ".*" '{"ha-mode":"all"}'
    - require:
      - rabbitmq_vhost: rabbitmq_management_vhost
