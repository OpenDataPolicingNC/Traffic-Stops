#!yaml|gpg

environment: staging

domain: dev.opendatapolicingnc.com

repo:
  url: https://github.com/OpenDataPolicingNC/Traffic-Stops.git
  branch: multidb

postgresql_config: # from pgtune
  work_mem: 22MB
  maintenance_work_mem: 224MB
  shared_buffers: 896MB
  effective_cache_size: 2560MB
  checkpoint_segments: 16
  log_min_duration_statement: 1000

# Addtional public environment variables to set for the project
env:
  FOO: BAR


# Uncomment and update username/password to enable HTTP basic auth
# Password must be GPG encrypted.
# http_auth:
#   username: |-
#    -----BEGIN PGP MESSAGE-----
#    -----END PGP MESSAGE-----

# Private environment variables. Must be GPG encrypted.
secrets:
  "DB_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMAyQKCZoo5mkcAQf/VkAPxauQQ71Zj90iuESa8GyLLq5w8AKuoqT206tm1RKC
    +bjz+lmRCXyI+g40x8YU5FXTtwkeXYeJ3YJvG6Xas+Vvs4N07GNUPBSXYu13NT4W
    ogI8+JHuOQvrRiavx2ygjKMSqmVQDPuJ6Rxn3P59l5durLoUPYP66AMy/VHrTZlL
    gtSZgOBaVK0RXTAREE3aBeNu30wk/tdPDzjKfidrX/14ofkCvR/vqhM68v/l9Bs4
    9YqbBqS8jEeR5GhSE6lJkRzpzNgGZXqjJUhlE6a/v4+lmPmQ6soHHUwfzDd6PryP
    CtBw5gpknS+VKFeQ4HfZ/o0pCIou5SvevCuef7fbRtJbAZc90wW2iqqk0fVgJCLi
    2ouV6rMfmgtMOg/HFG1GHdydgghHJrDA3MzRVF4LyFj4VYKmiZySskQ62fR57y5s
    FC3O2xFyo1Agzr1TLOxbSXE/SFhTaYhT9favnA==
    =3pmf
    -----END PGP MESSAGE-----
  "SECRET_KEY": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMAyQKCZoo5mkcAQf/XvZAz5/Nul57ysGtGkihXtm51scvvKuclBTft2m6lQ9y
    ME4Jeev4djZmjWJgkrlgt3nPW8xtmfcLHxUwKQNwzc/8aiXjWUEqqdxerigRTHDQ
    +P2jzE2OnYcqXEL8UQrEsL8CpiSK0l6VxKK2ENFZX/5ZnTB5DGZ8yUR1W3ylOeX4
    ifTzqRDZwyNqaL9Us4uEzr8RsqFWXUxpZVm2dIMJhBO5Vc4CheUH+Th4uoO4sgIT
    lMNj1ZlYSwoQTcbk9QGk5UIBnOKOZagS+qpoS4EIAaiZ/tj+WKORCW9bQYuPYoMf
    EvpF+8AxbJSOMHRMxBsWO+EstfjG+LUNXW2t0mA09dJ7AUfM1Y0iwzrcaUhOm/FQ
    eCbKl6z8X3LCgVIpr2ru6kfP6ShPDwiHF190f6eDIltEKFPE9kdvyHSG44YsWhQ2
    bZSSQpaQdHEurrPlYWIok+BlEWjyLWyyodnn9vXvT8Ngvsm4uOdZ4Wc3vY+Y5e14
    7d4ZGRdWCDx4ZSaj
    =X+bG
    -----END PGP MESSAGE-----
  "BROKER_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMAyQKCZoo5mkcAQf/SDk/+arGT0XzVVIwLSbW4f1/Z24xEsFAEhD54Wp5KSDz
    XxfDCfvUOz6TA4Vryvu2WqnhCvA+pI2FBsqkwhCYSkuDn1EJDMR7PFg9mijNpPM1
    xmMEJ89cB+46gfB/sNU6+xWFtZUp5igT4fu1j5PG9stdTgNM1TCmyAbE9rv5Id52
    zCMlDjqqc1ns0crM65mHNy8zQUs3WhR59IYCcZjhhD1a0M68B2GdqoSGC2GgENgZ
    FudKjlTEyer+c9iJEnBTrZA4rdTkdOcJzJ6hPrJc9m8uKZ5pa7xiLsDpwvN4evah
    qkeBxuSajFEboqsOZaexuVPwNZqKeSatnc9gr4plttJbAVl5IV8OgCAyYgmjVmHN
    5uqL29UKU3iTehG73Qi+zOtXgIrJl5nwuiamC2Btk6zqaSbGTxvJGomtw4b4uDAo
    7Z1IrjmWenrlJfL3D476W4nfj0KgIo5SV1+zQw==
    =TIUh
    -----END PGP MESSAGE-----
  "newrelic_license_key": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)

    hQEMAyQKCZoo5mkcAQf6A8lXWkk7cp8mbLFI+Fdn6cIanB0EGwDurkLW75O9R7JB
    y2G8RYKAV45/vdDGGSqZPThKSCA7bp6aAiGY6qhdRJuPmAMqdjNN9TsVgLETi1Si
    Pkmhy9RuNAp/07QFTe+Me4q/mwOk3nwDYcyaCEUtHXafWL5J+A6TvATx5RcBUHBl
    sz4ovcPS7P+q+NO1SoL8E2BQipwa+mcVzkazT7gSgi6Rtzf5H+aLf4SzgnVUHjFF
    bPOYus9sOv55guAK6OQcPDm5BeDBc6/6/P9Z7bse77uEb1x1HKxmTuEVNwESAbo/
    WZ5CRQxy9ihOlTaW7DiQkxtv9tUsaH17YrkHbWVBUtJjAaeJliU/srkiMX+0Ngpr
    2U8p7Atf4Hj+6B3qsDJ/FpKKJIrAb4otIkkRjhjLPPke4sREMFjO5Pi+1wBtlij6
    qzkPQs9tmiPhg5L+emKjQmCCTRCNDMORnf+Rbvfq5oODOQQo
    =e/BW
    -----END PGP MESSAGE-----


# Private deploy key. Must be GPG encrypted.
# github_deploy_key: |-
#    -----BEGIN PGP MESSAGE-----
#    Version: GnuPG v1.4.11 (GNU/Linux)
#    hQEMA4/oUOrM1wUhAQf8DcedhgvGDGsirvyivYTmuYjriZiESsPg3IYYRpZ+kVt+
#    4Spxu+qTPV9haWxporzOjtFDOrZTxuieVJQM3O9sPF+V7QI30BDWxEKSYS5MOiU1
#    i5smW6xiFfTkAFSLqEeqoLH2k1oKtJCygWIe38grTissteNVspUE9SdV+6XQDVeQ
#    D18TBbam6bM013GCOJ5Rvf7Cq4wdGx2+N2THfW9Dy9hJiIdQp6eJTh0wgwAyFm1n
#    QMZa9bv9h9mePzoHO+WdEYgFzJEIpSyYxNjB8qCy7wgb77qc4HimLseJHPWj6fIR
#    ZbVBa0aSj0jzbGNf7o6axuW2rCpaWSMQxd4toqIr4dLrAdJdJNA0RqcLN0E0JL49
#    PCn+/54hVcwBq3r/1n0AF5zXzT87Uf6wgPw2+UPOHknfQg4/qKtZwBWakdoZXmGE
#    /PADPGZD3RXYT5qnl35hqifVJMytg+VYcGq5BkTNb51mrH/VRldffFS7lHaz52kw
#    69a9sgK0zIDfwdqbukAnhaIyqZX8BG/PKSMTv1HWS7bYduZJgkomKqj18KoPEKR5
#    l5OufaTuNV6JRM4urcFxk7o2KLDdJ9AXHTiwOYJLtzWEZANSK4xU15ja+/6HzRw1
#    6EmGJFXArTf5loIj0hcYSGiapHypeRcGpolxEQh8rgMf5WKTGVkpqpVMzulzhF5g
#    uafHTIMgbBwTXbFGQjNVViBIuyBrJFJ0voIF3j/MX9DvwmfDcPEpK6b48cXMU4Zm
#    YPwNyLj/Wg3IQ+dRL5x6+Mvk22dUg4KWWvGnSk32s5Pm7DMKvLdCf/9/+8RZkAkB
#    mClFaB+Frms2i25esZUFAoAVnzvPQzeMHTwEAxkxTcR3UZtz8nG505Fk3o2WEtI3
#    0qV4Q305mDanOfPOCNTxVg/wiHFz3sYFdZotRKB+CfZ+1DS8nycf+2vOYg1LL5C/
#    zLOTfMsul0GpoTEVdZaE69y/iJca49SdAes/84rWNSA+HxxvLjiWRYJWFsrIWDQd
#    jkgWO6IJpy8KrhR9SR++b4x5J9VmM2nmSW366Ck7kTksTql+57gdBnEqTa+D8Nit
#    P+sa/qhEBhhsmVDzRqEQ2qy4p+n3ltwpWNXHlV/EY9SZ1vcksZo6bvYpEFfoDJ6X
#    gQPBb97qUmcHFikuN10KVL6PH+Jxdvq89eNgEZ9mvk5NPTslMEPWk3XyKMHrGQiP
#    DvlNBnBYmIH5knYLzg5RcDTGvDqc64RJnvOJB7kHfXDotzoeP4UXMvXUJ8z//T76
#    2IsyM36c9ox8A1WwtDpwshfhf28zpapq9o/PbTlnWwZEljJSZInHMvn8eeUG/ucd
#    8lHdaV/FSRdwm5Oxs1RTYzyaBJy4ZVAYcr3bMFcgp7ia+N+0ROIc1MHQqLMHqRRT
#    r8yqHad/SldN9pLbaBBexGjWRMWLvpZbI607YdrFHTN8bbP2zxpTE8wLBuyXuBU9
#    s7V5qFgq67y5glP4XVEeBFURJiizdOXwEl36C/8ZkGgqD1R0Ebv91rL2k+Wcy95x
#    g/2E9yk4YJ2bcVfS0bwYOhiZnhsn7Z4InGMAzXZIfydv3u6jUQv8UtZhDwKu9Qbx
#    EMVSHjHUxvbdRk93DIkgVrPlKzm2AN9oQYrCekUvkYTm/UT7JtvD0wfyvowuOMWA
#    BelrPgk2ypxn+h84uzCquHJPEyb0j4KbVGeB7FlcqNVHRMdCiQMW0N1CHVOFOPWS
#    vmydq9u8cSXwDuNYN5vMIQDS/rBF91M8uIXKWW4tj4Dfc44D7ZVquW88zg8uFJvt
#    38YyQA2PIXhOjlAhG5DGts5GRKi6IR+gfaGc7WxGWha2vU6hBRyg1Y9536qGq2AY
#    zMa7WSwSr6bFhNWXCrw7GIly2hk1Nl83CVGBqXr/iCEtzEaEvTm4cxq0x8iEMkVh
#    F1wlItO/RiOHviPi3VxATGUAoIitFUbih5l+XqBTpgivAd9x4s1SB9GaPnuDveZB
#    hzleHvb+5iRfpwWErYJKs+SXTErg0u66rRexCpjMpdxREQ+8MOQZRdfRqwV5yRTT
#    +sHpL3ABdjClYj7+NSJedSuw1rUq/GPWV7Od5qczyyEpoOnj1tcRuWxuYx9b5nvp
#    5K6atPVSQ5adal9xmUEMtlfqQpX82xK/edysPFHYhDfrDB32rOF1rQjE23fj3fUx
#    Itk8my+at/OJAa+WI+4i58xKQStm6GUyfBEr0gSDYmdfQZvbjSI/RMaYXr4qC/MW
#    bXVIIy8sO6wEz2mAyik6IJAFOu3OcmzY9f2H5rqf2Puz/GxvpnD++/gyGTWsUc19
#    GGXDXyoIa0zxHghvgnvmwwXkdo1FcJq1DOzDltzFmo1Xy32t5T3DZ3JKC86y1qZu
#    7+ILkiBrpul88QlG8JMH1RQUTY/wintYwHMFY6JTqs4LHbtXcisJn+AdsFF/p+bb
#    IEihSPjF84aXFW3l0p/ye6zFPHCb6ePu8P3qmNS01p3TMTIEDSiO3aXMTCSWeLsN
#    A4U2UVLaSg2Onvo1VYwESXuXw1f+BXLw2LABt2tc3dSHHaS2up2RPr3/E5rGP0G3
#    Wrb/eyxe0m1aPiAA5u6t/htVysB7M/aKVoiwFj0NEadTYmzyBtGLPQwfvw6imvH9
#    buoWl+SXg7pb/D4rwddMAq6nEbdPifxPQSw99LQ3wrNuiRchDn6u1vMutkvnlhVj
#    6al2PSuJ2G7Bh8YKkyjnJu4XmjaxuVIoYT6XUyJWjQdAyiHCg21Wc6Ic5xbJ6BBQ
#    cOYYxXHL+vQlGidOyFayklQUACMlqaPFMZseG5n0Mk1BMhRFOeAy8Zg2yavsl0gK
#    QW9J9aygkSh2hhbzSNBuuOnowzKTFhnM6ZE2eAEKwj+oOw1gGgZvXTqYzSjUDGr6
#    iDovfJfxuwmBqDZHgzthEx77jnGHaeOJuxcAx6krEFTb3E5uwsX0hr1o8Z3Ehp9h
#    MIvsARiaj/6zwZo+nt+3rL3cPkoEu3mxZy18w4TNJa3AkGDvZMQkhzZghz24dZJx
#    hh5iExDnaAClvpGEF12H9WBQu7kLzqw/5uieHGS7Q1zz3eGoty1NlHwTvnI+U+jI
#    zmaP7Hf4tk+RTZLyzfN6HhfBLXNbem68Fbd6/bB1PnZA40pq+4fpNZWD9yU02c1y
#    TFE41Qx5fUUKV1SwQZZd5GcegCFdZdR2yWyH0PUbNiUbebigv0dUkkSOZOIQfCX/
#    E1e4zbH9drHNk09g/T4fVlDKhvWYBEBj9Yf3qxmPSCiNchF5N97bcwMk8G3Ifaeu
#    wPPg0QYSY9zsm8TZ6HT+yuSsu3IHOLwIGl5Jeh8yFAB3Jdrt9PFefVLOE1gB6o/i
#    I3sWrjkkPGXCdKg8iikF9efoZFP0PbnX2vZ/7AQdIkYnLiKHPjaqP6UOKHcWgwzr
#    cLLCvz8NQYdev95wffG5algCgYIh7phad3+dxNcwhvC3hIxRxiDjkwSRvnGt5CgT
#    CFRtl4uAskIwP2DopN5P/XCOW8dmXSoL/2bEQYgU3Pq9jL1HfUyZM3e9+5TOsYRQ
#    9NBN7LvADLKCtq9zSMz5DvGZahS2bVH5YMil90gph22PLZoQb8K2pPtlPhJIolg3
#    iLc5zDwnjccp5oCNIqEnKe8dXP9sGVy5Nl5dh68U8m8IvS+C9ABIwIdLbD5OpkV4
#    NaUeCLpAYx8KkGZVf9tDAyAj7yJdIi9kjbNuviiqHfXiMeIG041lBFOUHQiOmC/q
#    opENY457b7YvA6TfplffGOsdoqAQpRkuPOI95WH3Lws=
#    =7Rc3
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
