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

    hQEMAxjKmUQTU68EAQf/THe354R07IfCkQrY2ksCMmuKWEX5h063hvY6nDPwGuaY
    QRzPbDjiLX5UK9esG7zIHCHgLAmG739rmP0dUDhk70aFp/rF11epLwsikkow3TRt
    RbO7xze3Mn17It8+sjix51PVAFfW0H2+whrjmESR7H5a6Db2jY9TJTkdLpunrxoz
    n71vfJttv+oUjIqrn2ZgUhEqGbUn3XD+nb9x3Uegx3x6TP1J42bIp/FX6bVqxpe0
    i8mqdrHNt0Hi1eLyAtdlcW4Z72gzsrzzcAfFWOoC+d2FIlgI8MD4HfmLL+LMOCfu
    ap9Rp+Xm5SRGXWRFuUyM5lE27eNBfWWW0wtE9cJ5U9JHAfjXmnk3GluZDPrBsisT
    vPnE29iEbNncFsml5x0J9Sk3BznadVNj7BVp5Kg0vTfqW2jdQWNj3nCtFVjnQ18g
    JOMEfH6eZAA=
    =pFcJ
    -----END PGP MESSAGE-----

# Private environment variables. Must be GPG encrypted.
secrets:
  "DB_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMAxjKmUQTU68EAQf8D9zfHdZHNJ5TReuIpHm+FDx90wh3ZpXL5PdYh+mQjB1O
    IjpNUBwlwhfRbZJAt21Z/xllMP2FNbQyGZjXz4M/HzEjNdTi1UffgS37ho/KBZHW
    U42ADUZZ2bVD5AaI/J7w74XLfDGgdpV6LOb6qG8JU1mpxGaLfQ0wxtXs4e8O5eA1
    Qv1uelcUNpi9bVC/yLUN0nOnLqPpuVd6EOeceol9h2gvjcnSo7lQn0pIw6kIsfgp
    cB64nreSk7juamNRwitTZbb+Fck45GZKY6QsFPIUJ9a1iNaacnRRx8etpl8owSUk
    5N+zgbc7iFQw1mJpMVQjH6ioQWN/Lh6G6zJidbKLbNJbAQXffnNgM1XBSBDnG15E
    fxabuQTQ3hHg5LVR86mcY7bGqOqCc5jbFDX9aiEPyyS7fv/eS7972iM9ZRATI603
    ZrHWSeX9O9MqYIBfa4Ugmvd9s/FaTCjss41jng==
    =AZDR
    -----END PGP MESSAGE-----
  "SECRET_KEY": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMAxjKmUQTU68EAQf/btxT5qXtalRNRsioIXYN+xAvrjAKOESfEEkR06g+5SdH
    5ZVVe5DQzAUR6Tl7/NlQ+0QHHE8cR+96/yzuJVIl80l8EOETCk1yp0+TCdv5f+F9
    nEm2Bz1bruKxNxg+rqW6VGtUl1GSwqrt2KB3r07Q34KLesNLG8+W4cAEdw01EXWT
    AghFRKOxPdS4GrBif9sgaIEZAwspT1C1vhNNwlhGgznkth3qynUQbRcdefCUjrO/
    m3t1tsxbO6kL7EtstZEDIJZGv90O/n/YYCROtc/AktpwB3i/arYJr+jtu3R+u3/1
    DPFoIZ9EsdsTmycWZP42d1fGWen7FLqSxVuv3BtMvtJ7Acskt7bow481Nk6/i1yQ
    dz5i0nzzP/yj/djPCWPyT0Gy/YHgLfemK4RPmwyNVZXgTTPrwQqNM294+qYF4HXE
    BaOqbjUO6PNtN0wni6z4CE2r20SY1AwDumKtbgRtEkgjEU155eEeo3uiLl5W47Ht
    WkoWkKysIy/PWsP0
    =O299
    -----END PGP MESSAGE-----
  "BROKER_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMAxjKmUQTU68EAQf/eD4Z+ixMyBi/p6ewRCuIPklXvYqxDP1oCSSEgesIG+Rd
    4ZIhkU29mBJBvlUsvfsVo6eBlXWoVCvGCRTPw2gf2PEbWkAXuRYdkBJoRaja+6F+
    9wGdPJ8psy5Tvr75ToYejyesRpzNNlocPos6wMV4j+bW0RvFgGo/UnsmZYIlKma+
    z188O/KgI8/uAvp18ctoQvCL88sqBlkYWtAEWRuXjyyq91cVzYkFgaIH38+wMLFX
    hr6cQnyEAi6Dao64DXfzQih0tEBebE5OWmXCzkKtueZBI3n/2qIkHVSXEGO/f8nj
    nueMW99OwfxIWJRUONjEqvDR6esO08Dt+UW6TdFQe9JbAW5JQf5i7KNsJoetAgDA
    g9lWQOUKj7X0Nqm7oLEosm2hDEL7eDaOztM3aMrMc962PQz56NRD/Z3Il2daxAoN
    4cpm0Ws5YeIEMZKcfVra0WBZauywuzfoSEYruw==
    =IcB/
    -----END PGP MESSAGE-----
  "NEW_RELIC_LICENSE_KEY": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMAxjKmUQTU68EAQf+Nri9PLzalzLTlsIG4UqKN4yHYCLkU1i/5w3zQXx0AMtl
    QDjroO4vU0sG1UloJHdhwA1vxMmhBenFjb/G2ov0xMBtrse6oR6wADKftV0+NJTu
    Vennq7z/7t6J2pHPROwu28CJ63O2M/NSIdb2Cof5Tl/fMdscd5tI+PbinRouFcWv
    Emlm2AMaJlqB+optWcJaaLN6hDRISbWLpsI3vkV4ObuLZc9Z+enwg/AHOibkAb5N
    pFE7BGq0RfHoP48ZiAVGBUwwdBEdYz7p5A12q5QKe7LGRUKvBb6LgxjX1uN50w2m
    dRtTmYYOcu6uAsbvNnZHi1zl3jbtviMgPR+X9DSYyNJjAQJuUEU/0r9pHuUGfi0i
    RLq8rVB3fiQuJaHOwNgl2e3LGAFP3XRLMM5m4TY13JHYoLtLNgZjlzYN3mBI2m75
    ecnfOyjh8K60sxsLpwTc/O6sxAmnOqWSvDJQq4eT0Uw1b6ev
    =XK6m
    -----END PGP MESSAGE-----
  "LOG_DESTINATION": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMAxjKmUQTU68EAQgAmQ7i8RXH58fSA7IEs4iQlP8U4d4nLxNAeQSQ7hJ4tdnI
    +moNVan83kJnc/dsMuumHVnQjjWaU6AsJ3jHWa3yObBj5lbXtZ84fHEflenbrZBC
    /tJY+zRAIcUpQzBEjRAd6K4Jhv0p3PCW/sJokYMTpu1ei3YyY3zm3avGUQplN+ZU
    zO9yInr1nOJ+cZTS4AC2iKIFrToXsCPso/sWEO7/YuagX40IdA5sAxdJU6LX/pfw
    vRSxldsCJzp7S+6/60JhYJxvo/eZJcS5L+UhMhQy5QUWG+azqOaR9inUPcC7LpiW
    00C3PrcP7nS6CSyZ0VdKIXnixWwG9WkKnA1H1w8Xg9JYASRj52OIE1zGfdspQq2k
    xWkRbk0cgtzofnp59Op71tHFf6IrZdSv/4TFcuaAI86U+k7cJKBAk1OaH/NiqCY0
    wI9Sk454Hb0PpiA28uugFa3irY8+pK1DbQ==
    =re1R
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
