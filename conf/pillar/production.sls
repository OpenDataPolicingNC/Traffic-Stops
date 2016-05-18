#!yaml|gpg

environment: production

domain: opendatapolicingnc.com

repo:
  url: https://github.com/OpenDataPolicingNC/Traffic-Stops.git
  branch: master

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
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMA+D0jX3LNz3XAQgArUbfRwgjmfRcVGuk+1DcCTA2Af1yB9LG2xMtMf7y37uj
    ilwNA+iMsL1+EfL1kTNdvyaBW7w/2yPJC++AjDiHdx7XEIe1lJbj7/M1HmeUEGrJ
    oQe4PTg6jLN0HifmqY0iwQeaQs+v8loTh97nE+CX9laU4gXqz0j4fLqpiMFvUEg7
    ViQtybzEZzxTSNDiTIOI+Qa0A/fz0eBb0d2n3Q0ItkynP5gzDz+5VUc7UNkVKFjL
    ynX/DkZQJlungPA46CuO23OXxI7+N2lQbXhXlK1EdfVQeM4B2eOr5YqtI+8j7DPU
    /v3uhhAM6q3OghQkMtATQAm/adVBtBrHAKXr0qxh79JbAYxujNrGjuDNdUEO55Bi
    ZjMei++ofSe9204Q1JvewWhIGrZ6HPwRPgaYAYmqZ28jeD2b9bbXpFdNZ2xpqb+/
    P3eDAxRxQ5/zsc1rMNy35K4J3iKtWEuHkfYKGQ==
    =EIkr
    -----END PGP MESSAGE-----
  "SECRET_KEY": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMA+D0jX3LNz3XAQf+J4swHDEZtPguuxKa8A9z/Mz/G7bkmD6sU6Q8NhVTcHlZ
    FTc9YkRai3Lk9zCYgFZJM2glAIjY0hbpe7BMoRWMRBGDKW0PPSdCrKHE15vyHQav
    DxieqH/W5WW2rloGKlcK5nLEDguDxO//v5mziqseOlhxkEGQbTTuzNxVn6xuQHH0
    wspci35b34ScGoBkjOqYmgHq84OeaYLKd9pgKkOHPN6EEqxwY3xyH0DEgZ8VbEFS
    RfKT1vJ9sKD0L9R6mrIeFNe68rCrdqMikagP4k5BG9LIuSC2THZGZ8UAh66kyklM
    AlhnTWQo0gMirlPLtdMVVHZlc6u6MBDZ5YyuuVpJ0NJ7AUoeKqG12PMphjIpVcXz
    Rn0KttzbTsqZawggI6jh45KXkyMKGAHM0hBiVxPB1iOR3+oNKaO6rTWhJnPZOfa6
    f6kAUuru6n7okCcwMjg2+MjLOw23VlUZ5B7HeVHOoHgRgE6+lPUcgQoGI/CKYWGA
    u3JqpQbtcw262HFN
    =VvKt
    -----END PGP MESSAGE-----
  "BROKER_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMA+D0jX3LNz3XAQf9GvAsb71hv8DwJ/B1VegBxISWPEfnpPsmYkuTRL8QKoGt
    ZAQf2RZPZvmuwr08r30Cih6NeYAP4n2UcJbhzVcYSAKZadZtMxPi3bn4cepMar34
    KvjQe7TRu01kNOzQPBq7u8giM77ZF5Se1ihiUavlZYMDDBhMrS6bRlmcxXt+/UAt
    2tugG3q3nD3ScPq+lG3bnMta/tglEsVvabosNR8/tyXXX3qC8fFtTCF3RizovL11
    ezzysBpirBWEx7LoWmWQU6BYqbVO1tWlg2qpaLj5VUzoapzetHEcvJMVuBBbETnD
    4NJIiDjxetRW4nrJ2F7EcLpxZnqtbZaj3w7wb96ZDNJbAUak0fyeQUyuJgEAH6EI
    XHLgWKZdriGpggc1wf4pyubGalK7w9MDaOfKavwwQ+uXX4tTVjqV/SZOpwD6wyV9
    5H7IuLIVew+DHpZMa3nZwhLreLc3vxQk7WCIfA==
    =boGZ
    -----END PGP MESSAGE-----
  "newrelic_license_key": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA+D0jX3LNz3XAQf9FP8q3ruyXGhlRH5ungo2qUGL0ucoQ9vu1c2VivJYACaz
    znPGrb4bduzwnkyCKUhrZ0fu9CCXPcvkhB9leCcgOKozR2BgtQetfaQVXVcAcbPQ
    OE8S0tx53Tp23phY7CMQN2A2FTiiciPR10Jv8k9z+qNPklkW+Oe6/kd5lu1XWm/G
    V/3oYTJQ/di48EqrzJNUg1gNVIZmVDthhNX2tEcBzfO0yaTBss+JyjSW7VnNyKpV
    VsSAnP7Qvl/aSarAP5ItWPNNiNPh10dYZip9ORKD4BZ6SohCd801pOwT+9rS8LOY
    S3HisVaXfCJLmh2M7+tMfVokLRXnT/KQ62/uT90P2dJkAbli9uyNuGEwmOoUYIAE
    ivpHmVslPvaqWgWlHniQyuvDeYbWgF5Ysv9WwCq4BSTNlU6m9rsEYlY/ANbLIDMV
    SOQeuLRN5v5VGKboYoSuU6kUNfAt9I+MFhke+D4ZLLFLVmD80w==
    =+5v2
    -----END PGP MESSAGE-----


# Private deploy key. Must be GPG encrypted.
# github_deploy_key: |-
#    -----BEGIN PGP MESSAGE-----
#    -----END PGP MESSAGE-----

# Uncomment and update ssl_key and ssl_cert to enabled signed SSL/
# Must be GPG encrypted.
ssl_key: |-
  -----BEGIN PGP MESSAGE-----
  Version: GnuPG v1

  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
  r1jBYzl8XAro4A==
  =3DZ2
  -----END PGP MESSAGE-----

ssl_cert: |-
  -----BEGIN PGP MESSAGE-----
  Version: GnuPG v1

  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
  nhcTxeLY62nNC+Tut120cz0I96bixA==
  =Qyit
  -----END PGP MESSAGE-----
