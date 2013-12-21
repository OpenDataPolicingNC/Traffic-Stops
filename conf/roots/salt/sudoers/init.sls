sudoers_adming_groups:
    file.managed:
        - name: /etc/sudoers.d/admin-group
        - source: salt://sudoers/admin-group
        - user: root
        - group: root
        - mode: 0440
