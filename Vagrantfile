# -*- mode: ruby -*-
# vi: set ft=ruby :
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  ftl_fork = ENV['FTL_FORK'] || 'ftl-toolbox'
  ftl_branch = ENV['FTL_BRANCH'] || 'master'

  config.vm.box = 'centos/7'

  config.vm.provider "virtualbox" do |vbox, override|
    vbox.memory = 1024
    vbox.cpus = 2

    # Enable multiple guest CPUs if available
    vbox.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  config.vm.provider "libvirt" do |libvirt, override|
    libvirt.cpus = 2
    libvirt.memory = 1024
    libvirt.driver = 'kvm'
  end

  config.vm.hostname = 'ftl-installer'

  config.vm.provision 'shell', inline: <<-SHELL
    sudo yum update -y
    sudo yum install git ansible -y
    if [ ! -d 'ftl_installer' ]; then
      git clone https://github.com/#{ftl_fork}/ftl_installer
      pushd ftl_installer
      git checkout #{ftl_branch}
    fi
  SHELL
end
