base:
  '*':
    - base
    - sudoers
    - users.devs
    - sshd
    - sshd.github
    - locale.utf8
    - fail2ban
    - version-control
  #   - newrelic_sysmon
  'G@roles:db':
    - match: compound
    - project.db.postgresql
  'G@roles:app':
    - match: compound
    - project.user
    - project.db.pgbouncer
    - project.app
    - project.app.management
    - project.app.management.syncdb
    - project.newrelic_webmon
  'G@roles:web':
    - match: compound
    - project.web
  'G@roles:queue':
    - match: compound
    - rabbitmq.management
    - project.queue.management-admin
  'G@roles:worker':
    - match: compound
    - project.worker
