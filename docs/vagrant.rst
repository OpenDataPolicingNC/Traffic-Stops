Vagrant Testing
========================


Starting the VM
------------------------

You can test the provisioning/deployment using `Vagrant <http://vagrantup.com/>`_. Using the
included Vagrantfile you can start up the VM. This requires Vagrant 1.3+ and the ``precise32`` box.
The box will be installed if you don't have it already.::

    $ vagrant up


Provisioning the VM
------------------------

The ``fabfile.py`` contains a ``vagrant`` environment with the VM's IP already added. Make sure that
the ``conf/pillar/vagrant/env.sls`` and ``conf/pillar/vagrant/secrets.sls`` files are up-to-date.
The ``env.sls`` file should be in git, so just make sure you have the latest version of the develop
branch checked out (unless you are specifically trying out a different branch). Get a copy of the
``secrets.sls`` file from another developer or by copying a version that is already on the staging
branch.

To provision the VM for the first time, you need to connect using the private key which ships with
the Vagrant install. There's a fab command which will work if your installation of vagrant is
reasonably standard::

    $ fab vagrant setup_server:app,vagrant

The parameter ``app`` in the command above refers to the name of the server in the
``conf/servers.yaml`` file.

If the above command doesn't work with your vagrant install you'll have to supply the path to
vagrant's private key as an additional parameter. Use ``locate`` to find it::

    $ locate keys/vagrant
        /opt/vagrant/embedded/gems/gems/vagrant-1.2.2/keys/vagrant
        /opt/vagrant/embedded/gems/gems/vagrant-1.2.2/keys/vagrant.pub
    $ fab vagrant setup_server:app,vagrant,/opt/vagrant/embedded/gems/gems/vagrant-1.2.2/keys/vagrant

Once the machine has been successfully provision, you can do all subsequent deploys from with your
own user account::

    $ fab vagrant minion:app highstate

When you are done using vagrant, you can turn it off with ``vagrant halt`` or delete the VM with
``vagrant destroy``.


Testing on the VM
------------------------

With the VM fully provisioned and deployed, you can access the VM at the IP address specified in the
``Vagrantfile``, which is 33.33.33.10 by default. It will also be available on localhost port 8089 via
port forwarding. Since the Nginx configuration will only listen for the domain name in
``conf/pillar/staging/env.sls``, you will need to modify your ``/etc/hosts`` configuration to view it
at one of those IP addresses. I recommend 33.33.33.10, otherwise the ports in the localhost URL cause
the CSRF middleware to complain ``REASON_BAD_REFERER`` when testing over SSL. You will need to add::

    33.33.33.10 <domain>

where ``<domain>`` matches the domain in ``conf/pillar/staging/env.sls``. For example, let's use
staging.example.com::

    33.33.33.10 staging.example.com

In your browser you can now view https://staging.example.com and see the VM running the full web stack.

Note that this ``/etc/hosts`` entry will prevent you from accessing the true staging.example.com.
When your testing is complete, you should remove or comment out this entry.
