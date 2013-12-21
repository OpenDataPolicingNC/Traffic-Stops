domain: events-staging.discovery.com
environment: staging

# git project repository
repo:
  url: git@github.com:copelco/NC-Traffic-Stops.git
  branch: develop

environment_variables:
  db_host: localhost
  db_name: traffic_stops_staging
  db_user: traffic_stops
  db_port: "6432"
