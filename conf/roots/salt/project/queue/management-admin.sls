{% set management_user = pillar['rabbitmq-management']['user'] %}
{% set management_pass = pillar['rabbitmq-management']['password'] %}

include:
  - rabbitmq.management

rabbitmq_admin:
  rabbitmq_user.present:
    - name: {{ management_user }}
    - password: {{ management_pass }}
    - force: True
    - require:
      - service: rabbitmq-server

rabbitmq_administrator_tag:
  cmd.run:
    - name: rabbitmqctl set_user_tags {{ management_user }} administrator
    - unless: rabbitmqctl list_users | grep {{ management_user }} | grep administrator
    - require:
      - rabbitmq_user: rabbitmq_admin
      - rabbitmq_user: remove_guest_user

rabbitmq_management_vhost:
  rabbitmq_vhost.present:
    - name: {{ pillar['project_name'] }}_{{ pillar['environment'] }}
    - user: {{ management_user }}
    - conf: .*
    - write: .*
    - read: .*
    - require:
      - rabbitmq_user: rabbitmq_admin
