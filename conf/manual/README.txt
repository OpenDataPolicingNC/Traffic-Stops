For production only:

traffic_stops-non-canonical-sites.conf handles the legacy domain names
[www.]opendatapolicingnc.com, as well as the alternate domain name
www.opendatapolicing.com, by redirecting to opendatapolicing.com.

The SSL endpoints for these hosts depend on the base Let's Encrypt
certificate, which must support these names in addition to the
canonical domain opendatapolicing.com.

The .conf must be manually placed in /etc/nginx/sites-enabled.

This manual configuration should be replaced with changes to the
provisioning to generate the necessary nginx configuration in an
automated manner.
