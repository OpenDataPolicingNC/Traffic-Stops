# if erlang.cookie has changed, we need to reset the node:
# 1. stop rabbitmq-server
# 2. delete mnesia directory
# 3. upload cookie and config
# 4. start node again

rabbitmq-reset-stop:
  cmd.run:
    - name: service rabbitmq-server stop

rabbitmq-reset-wipe-db:
  cmd.run:
    - name: rm -rf /var/lib/rabbitmq/mnesia
    - require:
      - cmd: rabbitmq-reset-stop

rabbitmq-reset-erlang-cookie:
  file.managed:
    - name: /var/lib/rabbitmq/.erlang.cookie
    - source: salt://rabbitmq/erlang.cookie
    - user: rabbitmq
    - group: rabbitmq
    - mode: 400
    - template: jinja
    - require:
      - cmd: rabbitmq-reset-stop

rabbitmq-reset-config:
  file.managed:
    - name: /etc/rabbitmq/rabbitmq.config
    - source: salt://rabbitmq/rabbitmq.config
    - user: root
    - group: root
    - mode: 644
    - template: jinja
    - require:
      - cmd: rabbitmq-reset-stop

rabbitmq-reset-start:
  cmd.run:
    - name: service rabbitmq-server start
    - require:
      - cmd: rabbitmq-reset-wipe-db
      - file: rabbitmq-reset-erlang-cookie
      - file: rabbitmq-reset-config
