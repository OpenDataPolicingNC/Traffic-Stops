#!yaml|gpg

environment: staging

domain: 52.6.26.10

repo:
  url: https://github.com/copelco/NC-Traffic-Stops.git
  branch: update-template

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
  
    hQEMA4+EmNPRUxq2AQgAxImnj2teryDdr2yAIbj9aPj9ue7c6E5knOo62fHCTOum
    DqBbibdf2jg27qGJ7XRSPivf/tD5e2jzqwURFWhzmiqspNsDV8DlX8fAt92dCqof
    6jftCEMRBE0cegCxcqJ3BmC5xI5MpqiV/kh7/KPHRsPKBYsc4rJRtxfPkRnbgmFc
    G2Nhxuq7N19t/pErLwohWi4IhMV88PzVWAt18ZwhOyc31Ko4gNI5XCcbtPs67+qO
    WF4t/pT78fUtfnjoBW4QCdXWaJSWQlqywYkHvIHnVucmSbYXtmVcfFpFEowC1yQg
    hJvx7obOA90YAK3foU2ya/IW//vActLasFw88P71HtJbAdFda4ukbo1D2Gat2s8K
    +oKyY2xWRlEs9NZPeMcfrhrWqDHjpe8BHFtrOn/1VOLPb+a/6MLUaL7sS8P3UstM
    t3+FEQ1gurzSr/OzX2Z9IzgXgLwbQRadp7bsAg==
    =eSaH
    -----END PGP MESSAGE-----
  "SECRET_KEY": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)
  
    hQEMA4+EmNPRUxq2AQf/Seoiyo9v1iTV7YcZr9qdf4KDLgugtLJ8x7tjo8nMb75d
    uovBX4xoWlTicEdcuyC34VUOayVLQGhqPsa6NETtBOJZ9s4YhHJYUJU0RuQCZT17
    oNTgFcGGs3wUChrY8tz7P1EmMVWwvLizxlfCUKDoDt4DxPhZGdm+xi2x/IUxcQoq
    cfFzAZ1E8eT3mnXkjowgfY3PtYm9jmgJWQGrK156wcfYb7L9rux228sCca0b9RxC
    QylVj73l9u/qjfCthFORLZ/d2JUuYgzmW3n7pgWYfI+/fPa3AIK9keUF+t/yATsl
    +fRjjAU0CXgYU3F281K+dqvsuv9iwGjkfcHhNT/UhdJ7AYZQ4UlqmeZbYMLnjol+
    oAM11hX/qDeDDZ6pXZRuoSjL3Eev7Dko/ZsyW1/Iy03sJrXQr1bNUUYkwfMIbHMX
    7/0sVCDRAjCxaVcvJ1dPDIt1vLrUCTtod8UygnIS7Ow45Gws+UA5gDawpXFZWx5g
    AfiV34C+5BYxqqxw
    =JBAK
    -----END PGP MESSAGE-----
  "BROKER_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)
  
    hQEMA4+EmNPRUxq2AQf+IaZHYiaeG7OtjTAHSwh8yklOVYMfuyEIewvGUVOtMWUT
    5Wq90TOTPAIoMxJS06Qx4pKYqsuEc04ECk6BgfamWHv+1YkEv6IjF+WHFGMa0kXj
    I9KDRGNikJ8mhtAbPAFCK+wKOXHHnFci1Y5JA5mKvrh4iGHnqprvnpbC2jV+6sV5
    3r+Uv3QJOBNMwKhpciix8VNShdheSOW55jGSvHI9ZF+y5zpGBX9ycmUJ8uJFfvkD
    vmrTkKc7XT6w5gakdrHNwIXWlyG+7OvObDaIxPco/IyWVNpMrWe3GZRKvvmOkSJX
    6O56j7OfkAFGMoEla4JqBeGuZGaNnUlhhOARja9uxtJbARp+jvki7MOVpR70syLE
    9y0Oas3cYgQYokuFEQlx88hR7CKk5D1+4wl52cTgG+7fMl4mLsCmF+N6SCRT+abT
    Qbac1zZiTpGZXZT6kia8hGofe4+TPniLx6OQAQ==
    =pNxb
    -----END PGP MESSAGE-----
  "newrelic_license_key": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)
  
    hQEMA4+EmNPRUxq2AQf/Yx9wwDUNUeZb0R7h2eeM8eFstrzckf7uWIkGwa7uDoy9
    jvvmHP+qxNoY1s6vISKZeDLi6nDhoI/lf799YBHRhL5KoNn+ov1jr6SJKGZ0GWlQ
    76FbO+T2Mh/LYeITAokFJei59cD9SF2Xs007H/B3qwhANOeZ4KATH3JWXXPoI3Xm
    SFTHC2niXPqJ5RsXwCVSn5cRMYV2Yoxi6UQKdT4mnP6n+KYSNwGEcQVjBJemm3ue
    ScvD4cSvW3Y5QyjuHyGsS4itK8GJxt2pY6+fsHtLPKBbgelZlh4YaFDvUFCwvm/N
    gV5IX8o8SGPo7B9bsXq7wQJdMPT5EDSpGFS1g9Ju89JiAetPcfP24eB7Hwxg2K5o
    140qo8VDVps3fUx+HyMxY974MrF5dXJ89UMR5EZg3SVfb4pvDUyNaDMoFPwfvrfK
    XIAUaXK9LkX2QVuw+2LBrR10o1ICycZN1oQ4wxUPGJbcUt0=
    =r+WA
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
