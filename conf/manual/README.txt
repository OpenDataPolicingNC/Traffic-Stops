For production only:

traffic_stops-opendatapolicingnc.com handles the legacy domain names
[www.]opendatapolicingnc.com by redirecting to opendatapolicing.com,
via the nginx .conf file traffic_stops-opendatapolicingnc.com.

The .conf must be manually placed in /etc/nginx/sites-enabled, and
the related SSL key and certificate file must be manually placed in
/var/www/traffic_stops/ssl.

This manual configuration should be replaced with changes to the
provisioning to maintain a LetsEncrypt-generated certificate for these
legacy domains.
