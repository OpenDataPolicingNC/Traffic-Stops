include:
  - locale.utf8
  - postgresql
  - project.db.postgresql.config

# mem_total is amount of RAM in megabytes. mem_mb is 25% of that (limit 8192 MB)
{% set mem_mb = 8192 if 8192 < (grains['mem_total'] / 4) else (grains['mem_total'] / 4) %}
{% set mem_bytes = 1024**2 * mem_mb %}
kernel.shmmax:
  sysctl.present:
    - value: {{ (mem_bytes * 1.1)|int }}  # 110% of mem, in bytes

user-{{ pillar['project_name'] }}:
  postgres_user.present:
    - name: {{ pillar['environment_variables']['db_user'] }}
    - password: {{ pillar['secrets']['db_password'] }}
    - require:
      - service: postgresql

database-{{ pillar['project_name'] }}:
  postgres_database.present:
    - name: {{ pillar['environment_variables']['db_name'] }}
    - owner: {{ pillar['environment_variables']['db_user'] }}
    - template: template0
    - encoding: UTF8
    - locale: en_US.UTF-8
    - lc_collate: en_US.UTF-8
    - lc_ctype: en_US.UTF-8
    - require:
      - sysctl: kernel.shmmax
      - postgres_user: user-{{ pillar['project_name'] }}
      - file: /var/lib/postgresql/configure_utf-8.sh
      - file: hba_conf
      - file: postgresql_conf
      - file: /etc/default/locale
