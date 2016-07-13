#e -*- mode: ruby -*-
# vi: set ft=ruby :

# This will setup a clean Ubuntu1404 LTS env with a python virtualenv called "pyre" for testing

$script = <<SCRIPT
apt-get update
apt-get install -y git build-essential libtool pkg-config autotools-dev autoconf automake cmake uuid-dev \
libpcre3-dev valgrind

cd /vagrant
if [ ! -d gsl ]; then
    git clone https://github.com/imatix/gsl.git
fi
cd gsl/src
make
make install

cd /vagrant
./autogen.sh
./configure
make
make install
ldconfig
SCRIPT

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"
VAGRANTFILE_LOCAL = 'Vagrantfile.local'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = 'ubuntu/trusty64'
  config.vm.provision "shell", inline: $script

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--cpus", "2", "--ioapic", "on", "--memory", "384" ]
  end

  if File.file?(VAGRANTFILE_LOCAL)
    external = File.read VAGRANTFILE_LOCAL
    eval external
  end
end
