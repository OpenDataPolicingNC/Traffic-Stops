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
http_auth:
  "admin": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMA+D0jX3LNz3XAQf+JJrGvQWrkRwNX/Fbqgzq2uCt47lN/AVWKgTUFyZGaVCg
    zpIvNma5hvX76XsuWdZ+1UcemGlkt8KaL94YDY3qsX1cEsjL3Kjo1JXW+QVf6TTz
    MKsTymYMW04enSUjw7VjClq7FwvXZpwZTgRZG3Z0JSwKN3BMv+2ipAd04TQD+pq+
    HK7y6DxouPqnF00X+IVYJsQqHAf2PJZUPCRa8Gizrq2DAM4Y4/vqVGkpb/muADKl
    1Sf37g7yHSE/EItYOSN08D5jVLhZIy5zINFOeiR8dpG823LQqYPj68vs7QMunLm1
    gQGZZ87VksG1GPcNQjFoOFQnJM4RiK0vCmIhNhEHitJHARD9Mo2A+p/Ii/sM2rXM
    9ykPYW27QJUptETRC4quwBMyyAMuvpazdExu8QvhTIOVUnzo0J30FtDo4yCHN41S
    bNNZZxnZrmo=
    =a3+F
    -----END PGP MESSAGE-----

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
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMA+D0jX3LNz3XAQf+JWQ4WvvFneUFk0cUL36o72IKuNa/8bYMfO0dQRYRzgsh
    g1jLz92SCiz0o8uGis8d9L8+gwjhfUGZvsqcOBK6D11xB1eGDE0L8NjiiSq7fPCG
    BzXQZlLt+WIIn/iOpSIDt8DQ/jA81Fx3Ja95V0OiDWbh0+YU2svYjbv9cnjJYr1f
    JE6OhpXUipxHiaf61H31OXIjgR3rxOs6xOcRDUCh+OprFHzoRMnBUlkGhTZzen/4
    8XvrZ9BJhk2HWyi4X00rymBKjlHWLawE7Y9K7ko+qA4ntM7gP8l5rrE1b3qSA2oJ
    eMasCtx54WhdMv1rWYn6mOa/blqevxLkvQAjsjwV9tJjAft/Ji7TS0PylbVWIL4J
    0CA2T5xVznjR5zL1+gi71kf1YpQq4R1MmIHlTJ/zYSJhUHMcyyWdJf5czlHf57MP
    gAv0wIhlGeVs/IRqT4Z6dALTtkYfhbGa34MlRTc5x9dP1cT6
    =aGnD
    -----END PGP MESSAGE-----


# Private deploy key. Must be GPG encrypted.
# github_deploy_key: |-
#    -----BEGIN PGP MESSAGE-----
#    -----END PGP MESSAGE-----

# Uncomment and update ssl_key and ssl_cert to enabled signed SSL/
# Must be GPG encrypted.
ssl_key: |-
  -----BEGIN PGP MESSAGE-----
  Version: GnuPG v1.4.11 (GNU/Linux)

  hQEMA+D0jX3LNz3XAQf/fWDPwXqKCS6WoeedtRMEOdfSPqZLW1KTOlfLASqd44a+
  wE44mOQ5hmgPHonIlaLqUsQu/UWeh2UUnyOI2MXLFHz+6kfKFbayknVFqeS3FGch
  lOMk0eyY4FrqbkyzQFDAm/8lQfnIhURWXt/iums47Zu0c7lYMaTzzjIIYarbrVPm
  S+Agkt4GSlrt1DMIqAxZ+iqDI/0aev0f/MDlCYCMjkzmwbH669a4/FbfgTySrlAP
  +CKcQ8m/V6gOqSFKIKeeHTK2oJ+NdxjZAvZM8YXko5u2jzF4AOcJa1Jv4QBUg3Xm
  XSsmnl2kelC/dRquE9ilp2UmKEllvaYUuWStsnr6G9LqAR5G9DTE+iyC9uyoSqBb
  rKn7VaL5uYfolVJmeQq4TD/2XdkgTftgwX6umJeB2muldklxbGqAgL4s2NaIozbH
  vynqwBI7t3KGRUXdMP0Hm8uKcdcdagm1eTrwB8u/YI11FXITYp+AGNRzaXOM9IMZ
  TJtsAogg0F8IsvFAySXsLkdNX+azQ0TkhsZDQPGJ7zUpQBt34A/DaXFUMAqD5Hk/
  U2heX252a3HHp555IiXiWrKdjR5W9R3m5x+CU4hviERuzelvP6qLwEGKXyQUoj/c
  7r7xMoteJ8jZ/I7Rhf22TX7qOt6pK4TAlxWDSB6Q8ecsWb1XlfuOMZB1P/pT9BRL
  Gcmq/HRPm0SD7/csMp3Uw2NoSCiwU1JOgNxgetyxtpaffDriRwIovU9Oa5wfShPp
  68ps+HehTEXIzQXFRYhfEBqYxSyJ1MHI24UGpV5k0QEF6j2sUZjnsclt28Di5213
  oLeNOmU947eHzeGNaYKTd6J4vWIqaZBhSdAdvh9OtaxRR9JeVVPALUul9rYH+mVd
  0hQmkabtuPZfqFoY1GIpik/tZWjgqumG4UuV6+wZGgseyWxOmlrCGMWaEkhklLSR
  KNP+b6k+IUs+tK0JQzhXl10No00QIHZVQfERuuOFSmaiPKqRJLAFr17QE9eR9tgx
  fRePJg3ef1niMHHdCxky1ZNQqwBAG/eWMlDuix8x/AbayT2lHqHR6NjlGfBWe/8Q
  C9P6bu5IdWgF6lJpmX5IYRudvJckWIQPrPx+JqBqVLVROvFNod52hfxYUKvFkHr0
  vNmwFhvpoXAs0UijGsa4VcxXg51Ll20GRcSrIS9We4DfRdav5WpkmlhNhlzGYo3c
  57fSWqiCJFcB3vB94h+tH3J4xmZcoyIHsjH1YTsjBJNfZEeML/21Bdv/dHiU/90X
  Pj6W8zTciwBGdYd94n027Nwe6N9PCz3O3MEw/KHcW/vvF7LV+t0xHhsClLdXLOsH
  ouk04Lv4rN8kEcBynytfRvLPr6RDs+Rq5lhUGp16t1plRy2K5W9V9Or0QMRjQuk7
  fL/WEZCimuoDPxjfQYpTTtpXJa3XarK0FEwzJWOYy1TyB/Mek8f4lfOc2oVztP4m
  MMXIQqstPsmYIXjvwbP/g2kJcGlZdt/d56UXoc5I2GCm2Auhz8TxcQoYI75s1a2G
  XbG4wZ/rWInNHgQGGjvRWvt4vJIMO/xatC+RUbwLMx5TFKJI7UsNcSJNFz0FJxHA
  rmsAvmkuHrK3g815RwYVfv/QbzxRGXsGrUkiEJuMRh3esj+ktlrzGMs0H2RHLzUA
  gJG+06w7TwiV1C4nMgC4husIG0Nuk28lRRtmjJzrJ0XoeGGCVRY1di0mDcnGbOgD
  A8CdO+STl1YCbE3Gw68MhfRnPOBZow0sg7sFg2OOxS+ltSP4f+ogCC4eMq2ggIPn
  +NhIz1tskmSLvcdWv97NZhSUapH4RiZ3Fg9EVbl31VD1eGnc8h64nWSBZfxZY6vF
  8jF0ZcnKXAIkuc+h/twQVri9RbVI/52jYSNLlFEVCFUPKJIXvVjuTyFE3EIpVQXZ
  IA5Su4iuU1kavSNmxcKK9790nPeyxDpKjZiuDNTkQDJsAo5GYrTgvc5mH+pNgDz3
  FYQGxBrVAoaaB5SM7l7/zd5Yb1a4/ZcsRsBoupdVl0i1FJTZSoiLpuy15seKDBID
  b3+xO8ji/f83yCYd73gc7Tp0NT9By1zDzUIFdn0D02oLM3NT/c7DYbk8zIefyMUs
  jnwraiJU3cKefVq2lRmTZwBhiWgOwP9he0K1PzKGPUedpPu6SITmJ0sPLNSsGgBh
  EQUmlKHJWvGJmmFJA51Hpw==
  =Fvso
  -----END PGP MESSAGE-----

ssl_cert: |-
  -----BEGIN PGP MESSAGE-----
  Version: GnuPG v1.4.11 (GNU/Linux)

  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
  =mgIE
  -----END PGP MESSAGE-----
