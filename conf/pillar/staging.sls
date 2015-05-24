#!yaml|gpg

environment: staging

domain: 52.6.26.10

repo:
  url: git@github.com:copelco/NC-Traffic-Stops.git
  branch: dev

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
  
    hQEMA4/oUOrM1wUhAQf/Y+/Th4Ntf1FIwal8ybMJGL18FBwCTp4b4wHjokEPpuQw
    zi0afUWcDkgQT6y/YuiAeRvg9RtT3SngAZapmav1zbRsqAaEzb055Bn0cZeCX11c
    vMNZjJHNakaH3ooM4f+qAniV5pbZi01y0eQ8RWg7LvtO0aMYUduq90GOdbaZiEC1
    5YG4ckh5Aq7m/rheVbq64eD6gZXbpHCR1OnYyYxmfSXLh9Z+LRycKtb42KU5ij40
    VzzBGfBJDCxPiLd4HRlMMQU5BdeQEMm7yITlkxuTsZoLcyiIG4R0GtuE4g6Vpdv4
    IlytYAIJqT8PsM7YMORmPorxu8P7HreRi6RWxdcHaNJHASVkABClIS/OdJj82hI1
    jJmQmBYD0zadXjU+8hpkLiu3ULbLfa7FJyQ45wURGis63BDwt5j47324unElC5if
    35RaKpXzOqA=
    =05xp
    -----END PGP MESSAGE-----
  "SECRET_KEY": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)
  
    hQEMA4/oUOrM1wUhAQf9FbMH8zeiqhVsR7WKD/79OsKy4VpOFbFlygyqFvC8RfYW
    aZxigTpGkpjWgE1OBw+oTe0D5p5WiuoI4r+S2yxPjGF+a4yKqTpYj2P1yUHYgbUA
    K7kwy7pBZYcbMRsTpWTj44KXuJgUjtzsrzSXJNErl/oeO24XO7TVjpYauZ37uZVJ
    aBxqQ/yOShaErfzcDBk1WX2T+fnWsd1YwfVpcPpExoz0IRkl08E1HGOorP6qquaX
    2gdU4IJx9qChfjMTCwycHe4djfoaAEvjb1wchj/KMsySy0cyaoKHwxC8MerYUK1Y
    uJXQi7jGdz/+g38MqM0TVOkqH5pwrNyr9YL57rf0x9J7ASYFW72zxYj2I3RVau5B
    BkpZNuALafsQGNoC8nCo6ProzEV3xemYtXFGswM6gNqTcH+2QTQlVIx1thJlHVUL
    x4lrOzwJurur388pDiSmpUl+Y9mlyblAW9eC4BG8eCwJuPVsiNJYLARz5CPUc4DC
    tDKOVU0nVK3vD5HN
    =2kGm
    -----END PGP MESSAGE-----
  "newrelic_license_key": |-
    -----BEGIN PGP MESSAGE-----
    Version: GnuPG v1.4.11 (GNU/Linux)
  
    hQEMA4/oUOrM1wUhAQf/SQphzZJOI7unT+Lu8v4/ck3RRSUBThSC+wBbfEDDL3IW
    H+tsGfvvsDNWnZSok1cSvHRU2soPHCYZT68W+OrZ+pT4LWydFJXhgHDES6r+tgNp
    sVsASSgUXwgOrWwowoISI/FwrJpRChjtpaulA9IXGBLiK7HGtdkdBK11jYZ4Nh9k
    sPFVMclmqGjg8Hh9GiUivOfdxqq+5ohzx/K6omMqBKIbt5n9pPgHA8R50FmJzfCT
    Bs8n/agLlDAvTPgsJwkFaBHZpZBO1Iyt7ZHBSPGEMYNPrWC1pPmOmBrZJlTTQTlT
    8Nq3CpZpxnJCjEHvhMVcqyLoBOVFAXYVIQrHgrP6vdI7Af0jRmuWbR2A/KgLiV+X
    VGLHCIin5aWMQyJp7zkVgZeGpRFeS9c49R4Cfa6bFTXgKo8LYuRYe+t/OQU=
    =ijyX
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
