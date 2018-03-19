#!yaml|gpg

environment: staging

domain: dev.opendatapolicingnc.com

letsencrypt: true

repo:
  url: https://github.com/OpenDataPolicingNC/Traffic-Stops.git
  branch: dev

postgresql_config: # from pgtune
  work_mem: 200MB
  maintenance_work_mem: 448MB
  shared_buffers: 1792MB
  effective_cache_size: 5GB
  checkpoint_segments: 32
  log_min_duration_statement: 1000
  random_page_cost: 1

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

    hQEMA0xWlbLrP5oyAQgAoRmV+IVYoYtPfKahirClWuvVP0z669OIXXkrQvTC4zl2
    5PEf60DZDIT8HcFZkx68r+IeETbUbFLCnrWv+JHOP4HaHb1RqdX7JRvIqFwE6ikO
    +PML8dXptdHNMpVfK5LZo/9xDGsrCYBGYgboHl8AqFk+rOLNvU9E6aHERXdeQ72B
    DFvnQdpHk48k9u81Z7t64e7f5RfNxtHobm5KUzPzedzxw64yIoIY3mRAafngD/+E
    05toByXps439yyX4dogqlq91pzlSQ195b2B/vUmNBD85j+ddgUMYq1FU4SQ5L7bH
    ZM0I+BJ9rjBEBE+2exYa+LlPyGhjYqJVlI6ZvX/oDtJHAa6fPC3ts3hI9bR+tVzc
    MfXXv604lOa2k4FhteSNX24Q9v8/BtRGg8U1CfHOSE91r/jKi/PALzM9Ff9P2e/i
    RCTSiofO3Ao=
    =wNKI
    -----END PGP MESSAGE-----

# Private environment variables. Must be GPG encrypted.
secrets:
  "DB_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA0xWlbLrP5oyAQf/SepLXE67D+SgJQ7qS1VsrlozAlqp/z3j2CHhhR6wMRtv
    Xzq93+tHPZg3yzs9iYr2oi6lHHUOjOyOHDftO6F7SBuKVl4mbtw0yVe89HJWuoCa
    wwxcfYVnWnz60CxrqPti0teTMNyC8985Em9tKpX8z+0eBfkW8Mux7XTwTNjUgLX1
    PcAlCyhMGjaQ67vgJnA1tVywOYcNuNCOV/3VOY2yJJ2Q1wIcyiiuaiWxzxQ7IebD
    3lzXoWZ4EzDy3JEuSFUImEzrwI8/id742wZ2+z4y3tLynmoFnkgRaLtW4EqsdxUb
    cNLaPEkP8/4cSP2c3CkIxNu/k1PUOL5VrGyc+Fg2CtJbAVP+vEVQRSr3JyBpg25E
    9kwJFvwgotzB+7x4blY+70BOayXA3oqmn7aYRscfdhgcB1Ynh2Rg+zPSKBctEXFE
    YIkmCeETF9D0X6iIddYDVe54fVNJn9n8ZRAN+A==
    =bXsh
    -----END PGP MESSAGE-----
  "SECRET_KEY": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA0xWlbLrP5oyAQf+NvaXGBIZvSzgXnFIIDQORCvolxr7iAnMRGcQW685bDMN
    q0HnJfaowPfVRhiD1kLcZ61GkErQeQnnUsLd5v0SpOHA4fJADRuVRITvcTCW2evA
    MLHB6JGUl8Hrr56JsD6kArKRFu7F89w7PSEasBir4fWP0vlaT5xZ/Vtm6MaCJ3Jr
    zycFwMNLszcn4QLCU18Vo+U6z90G/GTv1xU77a3PkC+GfVZMCbRqLm03pNyC++lG
    pqxG45jb596UG93MDHBOHDIOHc9Fb6rZkbPJr0xJjJtCjARRKbbQ7juzwTemAEyr
    kP8LipriHdQUtsIKiwrCsnNyECixSJE4gGKJL0cLB9J7AQcwVVzLYTTg6RkID0nV
    XDAvY5AJEFPjWBEobq+/TIp3rMoH+Ix5SwotvH8mahhFiuOW09ur33orYtTM3DhY
    pBbSnvtvQon0E9gq8uRqOxyvU5YwoNTm8BajkJrc7vhYikFs52TIyM6MxZxaNxDQ
    qoOMH+iriahfA+6X
    =FxxG
    -----END PGP MESSAGE-----
  "BROKER_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA0xWlbLrP5oyAQf8CvdQGf9qDch/z0XnCVfAxKEYztaYzjbb1BzFcYctP7l3
    YKiGVjwnhrPHxBZr5APBDA8Fqhs9OyOuKDRS+R/64ZVruOGJs/YKQ9JYyX4Vyotz
    d/3PydX2weOutdty85I5MdnxVWOGrbuUBozZBgVd+Vv/6+rMG1pJ9WaDw0c7GvqF
    4ZMoskiKIB3dGUQq4sN+W2EOOraupPgh6NJx2wOEVcQF9d2357dTbcAjIXLRdzx+
    SK8mxW3LRDah519laID9Vax9cGJSB/x6UavGtINpehzLtoQnKxBJzNwGcYZYtYzK
    eLFfOTczZKuoyDFal9prWzwwQakDNSU3IxSVaRWStdJbAcA4VqvPLODEHUEMc1IP
    iCl2htt/oY/ZQcALp2YocIEsrkdCBEz47OhsanARBqQGPd7RYZBQwvbGYpdia8Z0
    RrbGyflxizsSo+hhMg0yYBpkPsRTyLZbKoKK9Q==
    =6WvB
    -----END PGP MESSAGE-----
  "NEW_RELIC_LICENSE_KEY": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA0xWlbLrP5oyAQf+K/dNXlHn4qnS1U40EFuEIKfTcldrxiRMg4XXdzOgyerf
    porlUyd1eWzvMgA5SSsFF6giYc8PWl+8wqu/NBTGxJ8vVfZApVHKVpgwLHvpPRaQ
    nNsx/d5uSadtIaY8OMumfc8nDsE5W7XJHKq92FNgNuG0lC6ddFdGKnpsBsOHMxAl
    GAfabt6OyMMx/1OKNqI97eqj6QMhJ4Q826PyF5y9H9kWsxrV31737duEfMNwfhPh
    3qUZmcHkplpt6IRl3lrP2ohHC/nmuHrIix+Mgf+XHn4V2spQax7v+Rbca+nnaTYI
    h8ZVLMmyoJ4GhZJYpv29NhqB1Qt1t6z9ShQXqxvhjtJjAdTwtteR/yizvIQ9fC3X
    z2Q7+uWLAXt2v99DJmfJuGxeLLG+08tB1YbqygTL5W4zbAyF1B0carLPQhNmlG/q
    6c8k4LThUqWmrAOLAbi2kiBxtE7oy+CoKKdF/j8yHAcfBsaK
    =8lDG
    -----END PGP MESSAGE-----
  "LOG_DESTINATION": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1

    hQEMA0xWlbLrP5oyAQf+JHlDrVWoVtgHOpJCttrGOlmCAwA7hvMNfpRtQEZyBeiJ
    33zuw04vA4tG4uN+3EMesmehUzOqpjmrlL40U6pxBwmeDnKPjRsHVni1WIfWShPf
    TnY3iIbShoSONN+HhgmGontKHX9PvIHm7LNvwaQjVkNHIRT9wqqGsEmUMkNJr+Zo
    nSl9xRVXYAOfbH5fd2z1dz/gnB6a54EoTjvcJjxm3iciLNOrs9tq/K7vb0gGxr9L
    Znm/UGWGxGkbYhaEfDDBAivI6rCS26+CcoCFHvn2D03G/jwdIXNtuVSTGeKzwM0t
    sniD50dJoj8HYcI6gLwpjjNiDNsxscC+ifAUlKrYhNJYAdpLvu+HTjfCJyexE5KG
    SXjM+j4Spkk4iGE0Co3QSGHi9pEn3lic+m3vM525VFkMs7lOqm7tn0IRy63ReTIq
    aWOqR9w8I7jhbievWKUXBiDvidq0F7QWiA==
    =9z5n
    -----END PGP MESSAGE-----
  "NC_FTP_USER": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v2

    hQEMA0xWlbLrP5oyAQf+MsP+HR1Zc8ohXLxprj6zPJsJGHMngXRZBF+XCLFcHKhQ
    f1j2D2HEP/LqWDE7iihCvXmtZlMJH/DMcGGqTNiB5FIlnutG4vTg3xbFB3RGEY5l
    xEWCfjbhpVrfDiU9UGbaUW3JCOzFI1E0BPm00UmXu5+HXTbfMFP7ky9D3GykJEG4
    eyfkApeWUpcpHRTIVZy19fdPc9PSSr3H8vRKLlGg2G8ZS9LHFPm58Cn3KM1dt07/
    3aPpn4sFfhndV+GzoPA4yMcFSDA36TG6P4BNz+8Xur+u61LhnI+U6nXb0ANxJaB6
    6KrxKxrT4CytroP1WyMiNgpNV/tX76S2NndSfCO2wdJFASfBAGJ+2hi8Q6h2FNsz
    TyEn1CMb66UeHrS7UJmYneMv+RVnQvcF6yypdq28YDgsyR9EBGSD396x1EqRNaPX
    EcVANTvh
    =BZ0A
    -----END PGP MESSAGE-----
  "NC_FTP_PASSWORD": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v2

    hQEMA0xWlbLrP5oyAQf+OAQKVrmCn6feZTg3FuEsAf/WdyL8bZtE47TC6Lob5Vad
    X4YW1xWL+wz5DokwKwTHy9DYS5HpCqanqMd4zZ0HZzfGRiXpriMf9NrI6LgBZwVW
    tGjs8u9hS1EhjlQTDZdd3vIGhkXINK3niv6RoPwwMOJbbXZlT4LK/Zy7TGyF/Znz
    yKJiVEccMYeVyJ6OJr0uH78/fyEHEM7xar6EI79TFPbOM3uIz7qtRWIIqvOifj1z
    4CG30Xl9dX8e+9UrJ0/0/PTckedeLLWdBRKilYe6iL9Qg3VzCxCTuIvdfUPrpvtm
    gNasYYvyHm8nLJ523wtdS7wfcyx5gvmEIPIyu7egwNJFAf3+vsvRhyU0cVDzyCPh
    QVIT6A4H9vTU6cw3tLwB/NTlfpmG6hqEyhCZHDX7TQdJph61J0o9IGKMMKcsyDN7
    tJmBo736
    =VvCo
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
