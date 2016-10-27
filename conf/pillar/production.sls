#!yaml|gpg

environment: production

domain: opendatapolicing.com

letsencrypt: true

repo:
  url: https://github.com/OpenDataPolicingNC/Traffic-Stops.git
  branch: ODPM-169-new-prod-machine-swap-space

postgresql_config: # from pgtune
  work_mem: 88MB
  maintenance_work_mem: 448MB
  shared_buffers: 1792MB
  effective_cache_size: 5GB
  checkpoint_segments: 32
  log_min_duration_statement: 1000
  random_page_cost: 1

# Addtional public environment variables to set for the project
env:
  FOO: BAR


# Uncomment and update username/password to enable HTTP basic auth
# Password must be GPG encrypted.
# http_auth:
#   "admin": |-
#     -----BEGIN PGP MESSAGE-----
#     Version: GnuPG v1.4.11 (GNU/Linux)
#
#     hQEMA+D0jX3LNz3XAQf+JJrGvQWrkRwNX/Fbqgzq2uCt47lN/AVWKgTUFyZGaVCg
#     zpIvNma5hvX76XsuWdZ+1UcemGlkt8KaL94YDY3qsX1cEsjL3Kjo1JXW+QVf6TTz
#     MKsTymYMW04enSUjw7VjClq7FwvXZpwZTgRZG3Z0JSwKN3BMv+2ipAd04TQD+pq+
#     HK7y6DxouPqnF00X+IVYJsQqHAf2PJZUPCRa8Gizrq2DAM4Y4/vqVGkpb/muADKl
#     1Sf37g7yHSE/EItYOSN08D5jVLhZIy5zINFOeiR8dpG823LQqYPj68vs7QMunLm1
#     gQGZZ87VksG1GPcNQjFoOFQnJM4RiK0vCmIhNhEHitJHARD9Mo2A+p/Ii/sM2rXM
#     9ykPYW27QJUptETRC4quwBMyyAMuvpazdExu8QvhTIOVUnzo0J30FtDo4yCHN41S
#     bNNZZxnZrmo=
#     =a3+F
#     -----END PGP MESSAGE-----

# Private environment variables. Must be GPG encrypted.
secrets:
  "DB_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA40ZtB6LkJlcAQf8Cpvyh6K7TrGX1+kX2jnoXHIqUCRLIWEbqilhpXLQSSjX
    n1qKRYG69i+JaSI1e0UEmqu7piKRWeW8tqKCT7RBbxJmWKXU8fDhE1dQNor7xTiX
    jo7imCjPjNd1QHHvmtohviMxu2MOuuOsk76lhBdqrR9Sp1WJIhTA/gkEq49z0YoF
    QV7Z8u4Wf++96pcqAHKk3Qqat7QIoAY/+Vtc4jguNLd7rFnbDPIo2Cij1EK0RNaq
    9JVU83rMqbgv+CmMhUoqrvo4Y8V3jtm2SOANaAC22q1SAgUnYaWGwlg7Mdbo6/Zj
    rNNE3DOnZ9FWGJ+U4gy4m8NmbX8ES8WM8jNhqW0eBtJbAcUYP1H3q40Rfvdm+PGz
    nVptLA4oAN1N4Akan/0lLQvOiclV01fyaCkl4hJZVJiTMfvOJdv3L0rdLSbdcMdT
    d7uEldI4qOBKGk2mowOPIWWSLKVoz1fqBfnobw==
    =R6T9
    -----END PGP MESSAGE-----
  "SECRET_KEY": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA40ZtB6LkJlcAQgAhbGrjBWDUeWhrDM6kvRFtAV6XjuXmuBvQoGhjgQxxxeH
    8tsFISuk9UlWdRv40G0CqCAGiPypqlk/fwM762WkeL5bBUO1VIDt7l2ikSBzShDf
    v69Z9Sk5rvSlu+SnMFrd9IWHXaTA1/teYAZIjDaRJXgFCPr6c3UPN5BCUCT2YMww
    eqOFRUpAOAir5hRVsDsvgtmRhOkzy3TXEIejoeigcMnDnmynMxV5vnWHGxhnyfpC
    Dbad2uasxcqgBGXBLMmmSoQYf50jgDlaxJxLi2Q8Fg0a1Ui6hkRtnfsEn3mVfaD8
    QwyRy/HA5wj0bsc8YzqhQDVtQ7vIc/vMyhpZCncGJ9J7ASqH9SBUK3cgFDDUBKv3
    WaaJGHNLIlMwzXZGGDy20nIXxyEs0+hyAzPEXu/+9CzCqVgs/DUrB5MDO2KfJNgE
    Udc064dI7ChpuPyTgBtEn6GfkDEMdgMl5JfU0DomQsiiQ5usC+LTCNtWGTCquzIG
    1T1PqtBDaetxZKhL
    =M0WV
    -----END PGP MESSAGE-----
  "BROKER_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA40ZtB6LkJlcAQf/TpV0gJVnDECWZhA9gGR9laBK1OM2Kg79YWRrTqlU95WQ
    hX8S3Uofziy3AjCSZiJxc4OvX/MAcCRGDTWhIZQCwqyRlFepNBJzUFGNeEsytMOA
    30IpcbRoxiKrxP46yYdpnLmYPvq7ehdi+acC7t+ek0Ng60Y8mihbpESPuqbN3XFZ
    fxzPSjZMx7Fk/4K9CVFtl2vkRT8v+zePfBpkQH/Cc3ChB66/dWLpEyY1uasnQc23
    O3vU1FotlpOUR/Po/gd2tLAcrxzwAclr28FXTNs9lgqtVNUWMs+UwZEq7h/oNhqm
    Mii9ygQrlul7Caz51uxsaaO7X3Wg+ist/PwsWJDeldJbAeIypOXO+cuy0UslzbGD
    lA6wU7LqDo6eSHxTXXi1hn/XOYzrmQrC0Towa+MN/JZGfpXoz0PWgjs+CECgQ9iY
    UU+l1wmIKtR1OMBnkeO0WtzhbAcPQ4iCS3Ynpw==
    =6NJR
    -----END PGP MESSAGE-----
  "LOG_DESTINATION": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA40ZtB6LkJlcAQf/aVA4//E4NwGA6eKdETs+G0MJsIHphGlUb/YzUPqPLSiu
    AtjX4FPd7pFa3SLP2rJmeURMLFtHrBwfiU3/fg/+SxMF4GbyRp1oh1c7wLucwF/j
    NbTvP/SLpeY5GIYosZNKfTHb/GXXKzAN3tKAD5YVr0Zwg6q3/ZqKstLJ6wRSaP8X
    TNd0FiG4fZLhSsS7wtnzp7Wb1YnOKOxW1x/wsT/vIP84IguAtGJRn5+UUcz4zRjW
    v+TQ+u2o2trD3rAVSdcvAgYPFt2p6wY2zQL7r4dEiZu2fBud49GKusr6Jos04QpM
    DB53IR3yjdQR4FkZnDv//Yh+trcUPGFXEgOMzXDsm9JYAQmPkz6r2yh616gT3vLK
    KS0wf7fE/b0NWAZ30l/eVBhVQsA9Fj2/UuWpsBBzf3yH+EXt6I0qv5VAd75qr5G2
    88lkONnf1l8kDs6ALoG+Ri6sptEAZH9yIQ==
    =dNgm
    -----END PGP MESSAGE-----
  "NEW_RELIC_LICENSE_KEY": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA40ZtB6LkJlcAQgAlN2MfIJyA2H48L063ftJWW5TFA/d44A4xj3/pXtSd/VR
    H+ukkXu/A/w9uuFKKTm8yUsIv+5SvFEGh9in2BSgZhvP7fcXyzyaYq2G5Jd2yrpq
    LKsL5h5Itntr1Q0paurBj4J9pcYZeFUJLn5qf7zkfdVzuzwRrhqm4ahvUAghtpN4
    OBZp7XsIkDjlB6m5J1IAeXH9s29f1IgLeRtRqejV9a1icbWMu48Mpt82rE3H1nLK
    1kogR+pExEe0aQM6B74i2nPQNGWii8gJZE5A2QIwpVe5XGVFIpYnZt19jA4fCcox
    JCa5I3ir69PsKbBbJQghBLgp9q5tULOeZm1A/MG6UNJjAWDxLm6mijEi1ouGJUaZ
    d0ckWZXoo7xRobLOtA7G/uVtyRv/L1HZzfAkLBfdiSOLblhxCmeZID3xrFzAqPIr
    JIHuRD4M9IMa0EpZnSeQf2t4+TA/4Pm8DAHS+gBju/ZlK+2k
    =MHLS
    -----END PGP MESSAGE-----

# Private deploy key. Must be GPG encrypted.
# github_deploy_key: |-
#    -----BEGIN PGP MESSAGE-----
#    -----END PGP MESSAGE-----

# Uncomment and update ssl_key and ssl_cert to enabled signed SSL
# Must be GPG encrypted.
# {% if 'balancer' in grains['roles'] %}
# ssl_key: |
# -----BEGIN PGP MESSAGE-----
# -----END PGP MESSAGE-----
#
# ssl_cert: |
# -----BEGIN PGP MESSAGE-----
# -----END PGP MESSAGE-----
# {% endif %}
