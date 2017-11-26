# Class: laces
# ===========================
#
# Full description of class laces here.
#
# Parameters
# ----------
#
# Document parameters here.
#
# * `sample parameter`
# Explanation of what this parameter affects and what it defaults to.
# e.g. "Specify one or more upstream ntp servers as an array."
#
# Variables
# ----------
#
# Here you should define a list of variables that this module would require.
#
# * `sample variable`
#  Explanation of how this variable affects the function of this class and if
#  it has a default. e.g. "The parameter enc_ntp_servers must be set by the
#  External Node Classifier as a comma separated list of hostnames." (Note,
#  global variables should be avoided in favor of class parameters as
#  of Puppet 2.6.)
#
# Examples
# --------
#
# @example
#    class { 'laces':
#      servers => [ 'pool.ntp.org', 'ntp.local.company.com' ],
#    }
#
# Authors
# -------
#
# Author Name <author@domain.com>
#
# Copyright
# ---------
#
# Copyright 2017 Your name here, unless otherwise noted.
#
class ytlaces () {
  user { "tsutsumi":
    ensure => present,
    shell => "/bin/bash",
    home => "/home/tsutsumi"
  }

  file { "xresources":
    path => "/home/tsutsumi/.Xresources",
    ensure => "file",
    source => "puppet:///modules/ytlaces/.Xresources"
  }

  file { "xinitrc":
    path => "/home/tsutsumi/.xinitrc",
    ensure => "file",
    source => "puppet:///modules/ytlaces/.xinitrc",
    owner => "tsutsumi"
  }

  file { "gitconfig":
    path => "/home/tsutsumi/.gitconfig",
    ensure => "file",
    source => "puppet:///modules/ytlaces/.gitconfig",
    owner => "tsutsumi"
  }

  file { "/home/tsutsumi/.gitignore_global":
    ensure => "file",
    source => "puppet:///modules/ytlaces/.gitignore",
    owner => "tsutsumi"
  }

  package {"openssh":
  }

  file {".ssh":
    path => '/home/tsutsumi/.ssh/',
    ensure => 'directory',
    owner => "tsutsumi"
  }

  exec {"ssh-keygen -f id_rsa -t rsa -N ''":
    path => "/usr/bin",
    creates => "/home/tsutsumi/.ssh/id_rsa.pub",
    user => "tsutsumi",
    cwd => "/home/tsutsumi/.ssh/"
  }

  include ytlaces::laptop
  include ytlaces::xmonad
}
