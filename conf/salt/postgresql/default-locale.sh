pg_ctlcluster --force {{ version }} main stop
pg_dropcluster 9.1 main
pg_createcluster --start -e UTF-8 {{ version }} main
