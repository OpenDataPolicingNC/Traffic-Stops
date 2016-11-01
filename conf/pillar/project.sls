project_name: traffic_stops

python_version: 3.4

less_version: 2.1.0

postgres_version: 9.4
postgres_extensions: [postgis]

python_headers: [libxft-dev]

margarita_version: 1.7.5

admin_email: ccopeland@codeforamerica.org

# Celery tasks run very infrequently and use a lot of memory.
celery_worker_arguments: "--loglevel=INFO --maxtasksperchild 1"

instances:
  - nc
  - md
  - il

env:
    NEW_RELIC_LOG: "/var/log/newrelic/agent.log"
