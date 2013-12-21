Server Setup
========================


Provisioning
------------------------

The server provisioning is managed using `Salt Stack <http://saltstack.com/>`_. The base
states are managed in a `common repo <https://github.com/caktus/margarita>`_ and additional
states specific to this project are contained within the ``conf`` directory at the root
of the repository.


Layout
------------------------

Below is the server layout created by this provisioning process::

    /var/www/traffic-stops-<environment>/
        source/
        env/
        log/
        public/
            static/
            media/
        ssl/

``source`` contains the source code of the project. ``env``
is the `virtualenv <http://www.virtualenv.org/>`_ for Python requirements. ``log``
stores the Nginx, Gunicorn and other logs used by the project. ``public``
holds the static resources (css/js) for the project and the uploaded user media.
``public/static/`` and ``public/media/`` map to the ``STATIC_ROOT`` and
``MEDIA_ROOT`` settings. ``ssl`` contains the SSL key and certificate pair.


Deployment
------------------------

You can deploy changes to a particular environment with the ``fab`` command.
The files under ``conf`` are rsynced from your local system to the server on
each highstate, so you don't necessarily have to commit changes to git until
you're ready.  Code files under directories like ``traffic_stops``, however,
need to be committed and pushed to the repo and branch configured in
``conf/roots/pillar/<environment>/env.sls`` in order to be deployed to the
server. Here's a basic checklist to get started:

* Your SSH key is in ``conf/roots/pillar/devs.sls``. Another developer will
  need to run ``highstate`` on the specified server if you're adding your
  key for the first time.
* The git branch you want to deploy is set in
  ``conf/roots/pillar/<environment>/env.sls``.
* All appropriate secrets have been entered into
  ``conf/roots/pillar/<environment>/secrets.sls``. ``highstate`` will
  automatically sync (but not replace) the remote ``secrets.sls`` to your local
  checkout.
* The server you're deploying to is listed in ``conf/servers.yaml`` and the
  minion on that server has been updated with the latest config (see
  notes below).

The full Salt state tree is rsync'd on every ``highstate``, so you can deploy
locally without committing any of this to git. However, any code changes within
the ``traffic_stops`` Python package need to be committed and available on the
environment's branch specified above. The following example assumes you're
deploying to the ``app`` server in the ``staging`` environment (found in
``conf/servers.yaml``) with a minimal Ubuntu 12.04 installed.

Now you can deploy with ``highstate``::

    fab staging minion:app highstate

This will execute the entire Salt state tree and includes updating the code,
running migrations, and collecting static files.
