#!yaml|gpg

environment: staging

domain: dev.opendatapolicingnc.com

repo:
  url: https://github.com/OpenDataPolicingNC/Traffic-Stops.git
  branch: dev

postgresql_config: # from pgtune
  work_mem: 44MB
  maintenance_work_mem: 448MB
  shared_buffers: 1792MB
  effective_cache_size: 5GB
  checkpoint_segments: 32
  log_min_duration_statement: 1000

# Addtional public environment variables to set for the project
env:
    NEW_RELIC_APP_NAME: "opendatapolicing staging"
    NEW_RELIC_MONITOR_MODE: "true"

# Uncomment and update username/password to enable HTTP basic auth
# Password must be GPG encrypted.
http_auth:
  "admin": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA9cHY9yQNCWgAQgAmhpdm+tjKESsQL0TBMBBXfpU/L0My3FqWjVIDRcJapXn
    HTaWjESVSe5SB/hxeS2WcKqeZwz3h6M9Hspzyim+6mZBbBa8PPYVUmtH/62QiKAj
    lzBqEqx5ZQo02FZD6WbUTUgs+ucSYtVHTgNQMqDKdDUOcnD5lGdif730N6WAgCdC
    sVd6Ham4yyyhPhEZcpF9szvFaks5hyOOTn8+tmPpW5KPLxNSQ4wGkY9YXyVwJwkl
    aNhmCV2S0/6lDCDRURVFdACJ0jzWRhW+aeaENbaBEHRRyw2Ja2UiSXdjhKOHI9Yk
    6iwMnCKIxjge8toR4pGoaEiaAYuZtieVUCezgKLyedJHATAUZYdteoFPM0TLK77L
    0JXJD5U4rug+C3gNJqyJLhTtuCfe8K9JDT7wr49YrHr0naKgai4QuPaWTl57Hv/+
    WXJaISbHNcM=
    =8xCK
    -----END PGP MESSAGE-----

# Private environment variables. Must be GPG encrypted.
secrets:
  "DB_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA9cHY9yQNCWgAQf/YhJIlQls8V+i3IZONkGf4hfdY9eiPG+18abjL7a7tzPx
    sqjnksLzhbzt3s6p1yqms57SRtt9SbqyI1QZrNHu+gPMq/wmhiW1Uh4u+AHczQ7L
    y1j5KGqlOgYTNyYU2AJgVamk+5MAALshsNNklW8BBFa0jZolUsC2aEJiUsds/icb
    ICaEqVrgWBzWvto8If80hflkoUSKnlgEaMb+DFgEpgiG2y0fgJ42taiGwIisABTi
    p1X76pS5+XFN2w3nRTqYz4AAj2cCdFK8ttEP9xUsWHRIBPN5ZkN9/bDq9LeVmVtR
    I7/wYiVS/l9d11r22Rt9vIuZAgtBxdD967OwHYiyndJbATzuGTSndnwWhr/QeUc/
    Fka5LpW4D8+i6yQcYrUHp7thYqC4nxKlyRHR+f5PByiIas1xJKTnu9ezpP+glGdc
    OgLKEdD40Q2Om9mPGkZGDetRSlsuEz+qtmtLZA==
    =WPc7
    -----END PGP MESSAGE-----
  "SECRET_KEY": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA9cHY9yQNCWgAQf9FHHGpvEpbFPDwcEBBepGiW4yzueQHk8i+Fiyzyz7DguD
    urlXGnDsiEbN1IoOySmxxr6UM/Y+PscflCDpJF5po7obd5loIslVtw/m4gHm2xoN
    VA0Yh/M2K5JW5KZHz8wanZVVlZfYmY2XV57zRRhGEKuvd6wv08GpDqZNA0V5HRV0
    76cpK/LKgHnxllwhmEWkL327lVpgepiUHRrVlSmK79MgobM04OGSocJJFCLGfKGH
    iZ5rdpNSdcsMzzGIt4PJkifCNEhSMVvBLJoApVNpZU9gsmGnTbe0GHbwz4RVzht3
    pnSR0jcv1N8XCNQ4+oviTHWCJoQjMlco9+facqBG3dJ7AUxtNKOAOCbfWa0D/e7D
    zcucrd+OvIViqTCumzC76Pb0DVVr4xXAzoMi4K2IK6TgzqhEML7lbD0uB9tcud2l
    bUKkZwzLfp9LNGlswFt3pzfcEFzN/3tPzPiprWhu/TdsLYX1fen8QyiTRnKl36DG
    X7PPWbvGIM69iiLf
    =3o8w
    -----END PGP MESSAGE-----
  "BROKER_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA9cHY9yQNCWgAQgAivcRN57iy09wiY2qs7pgt5nkNd0ci7RHj3TWjhj2gi9O
    G6J1SLaV0EsEjD2I/x0k6X/uAOnw0iN8BNdULurtHcNYBXrcCsuozpwkGDbDOW/j
    ks2Svuo8IC3jTUfbdYgCyEYH0SXM1BngEqeMF3IwTo6P69SkP/qUghfCKJmOTw01
    2KqmCt/xUT1/hb6qYZMngf5WE+5tnFfBhlJJuhQQZVGWuG3Xu6NZMWewm2eFIVxy
    hFpLPzPWnf8V3TNdHqw9/5gcFLhfEZ8vI9iMSK1yELSpan1SXpUQgLgq01bhuYIj
    kxFzePJO3y9+6MG5pGM4vPCHn8S77C7CR/2CA0WgmdJbAbV56fUzKi88KXOK6e9J
    SXcegEGkm7QiMr+VSK7uKB5n+6EG0BCTm2GOBissimwNnlYaDOA9kGaKsCbGJpHr
    K7Npp/dU8bJUgFPZVfG/aVYvGSlGIpU7IKsgoQ==
    =WVGl
    -----END PGP MESSAGE-----
  "NEW_RELIC_LICENSE_KEY": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA9cHY9yQNCWgAQf+M6klDQoFUGvGpCcAWvo+FfoM0r9/gcq4lct/WAOsIgex
    qLR+CcVVE/luool5hcxQ7UUsnwksK42phYXGM75hq0ncYWesYBE43zHm166wSn9p
    PGf0ny27ii+WivyIj77IwVoqa8nLD3PAr7zkIazy3UgKuLZg24LWDkwOxTpFSn3v
    Ux58ag4CRqzdJTVRkwACTgQsnt/ggoP7QaOe4RZ8DSRDNy9INO0TpD8wQRUVmrEX
    murYQNAcNCONthEEpp+yND1W+4FBwLuJnqCRt008M6oVDHN6e9W3cTshxceg7zG/
    Bzz9qJB0Ql/ooqqMPPomCCORp23bW/yoMhEfarU/MtJjAd4/RXb0U57bDxa/VxPn
    JzMQ2tOaygYQpzcuuegTL2m1cfXhyNmbuUvUvGS32wL4ZaksirHKPG7sROa+DTQG
    ASDrqtsT0V/Wydp/lkb3TBVRnS4QBdm+oiVouZel3R46LX8r
    =AaNp
    -----END PGP MESSAGE-----
  "LOG_DESTINATION": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA9cHY9yQNCWgAQf8DvxwyqzKBQgn+w9Q0czkgi+dwVzp+vcu5gkycwvAHaQ8
    eCMgnoaf3sVdY0z28WOirAUCO6Bfhr5e/EP5fMr1bt/nLvMNTHN7DicGEeS4M5js
    mtteeRSlxc9F7+CxYXNzlMOjBNIpMNh8f4IKdF39I3SVUakgbsO2IfvLBjqcfqJl
    L0wr7N7XC9E20xNNWEmM8FJSFY35is4kuND8MhVNDQXx12amQYkDCW5HyzaOw2QB
    wYh6x1EHBaYkLECiGe9vcO/ZzugUmbMlN+aHtKVA5moQK/V0pUrkU2pnf1bG7m4E
    Tbws/vKzj18GKhHxTqhX+hDNiuUabQkCn6UnE/N22NJYAVldP5m8lUkXrsuv9dk8
    N+LqsuwuFujZei23HqHzSgvHAQ1qLLNg2f5apmqu4vTK0na3vq0M26VtTwbppk29
    wxuHWgjzG80PFEbJfVa+0ufsdYPBEVas2w==
    =NIlV
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
