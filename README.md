# laces

## Installing

* install puppet
* clone this repo
* symlink repo to /opt/puppetlabs/puppet/modules/laces
* $ puppet apply examples/init.pp

## post-install setup.

There's a couple more steps that need to run, post-install for now:

* add a section into your bash/zsh rc file that sources in a whole directory of rc files:
