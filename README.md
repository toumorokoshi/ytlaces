# ytlaces

## Installing

* install puppet
* clone this repo
* symlink repo to /opt/puppetlabs/puppet/modules/ytlaces
* install the following modules:

    puppet module install puppetlabs-vcsrepo

* $ puppet apply examples/init.pp

## post-install setup.

There's a couple more steps that need to run, post-install for now:

* add a section into your bash/zsh rc file that sources in a whole directory of rc files:


* add a resolv.conf line for google's 8.8.8.8 dns. This ensures that a public
  dns is used before a private one.


## Setting up from a fresh Windows install

* run disk manager ("Create and format hard disk partitions") in the search
* shrink main volume by desired amount.
* disable UEFI secure boot (arch linux boot will not start without it)
  see: https://wiki.archlinux.org/index.php/Dual_boot_with_Windows#UEFI_Secure_Boot
* start arch linux boot partition
* follow setting up arch instructions

## Setting up Arch

* wifi-menu can be used to connect to the network.
