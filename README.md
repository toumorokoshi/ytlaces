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
