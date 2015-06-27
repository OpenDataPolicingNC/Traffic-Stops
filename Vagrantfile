Vagrant.require_version ">= 1.7.0"

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network :private_network, ip: "33.33.33.10"
  config.vm.provider :virtualbox do |vbox|
    vbox.customize ["modifyvm", :id, "--memory", "1024"]
  end

  config.vm.synced_folder "conf/", "/srv/"

  config.vm.provision :shell, :inline => "sudo apt-get update -qq -y"
  config.vm.provision :shell, :inline => "sudo apt-get install python-pip git-core python-git python-gnupg haveged -qq -y"

  config.vm.provision :salt do |salt|

    # Config Options
    salt.minion_config = "vagrant/minion.conf"
    salt.master_config = "vagrant/master.conf"

    # Bootstrap Options Below
    # See options here:
    #  http://bootstrap.saltstack.org

    # If you need bleeding edge salt
    salt.install_type = "stable"

    # Install a master on this machine
    salt.install_master = true

    # Actions
    # Normally we want to run state.highstate to provision the machine
    salt.run_highstate = false

    # Default will not install / update salt binaries if they are present
    # Use this option to always install
    salt.always_install = false

    # Gives more output, such as from bootstrap script
    salt.verbose = true

  end
end
