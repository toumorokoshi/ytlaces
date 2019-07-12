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
#https://github.com/tegan-lamoureux/Rotate-Spectre/blob/master/rotate.py e.g. "Specify one or more upstream ntp servers as an array."
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
class ytlaces (
  String $type = 'desktop',
  String $username = 'tsutsumi',
) {
  user { $username:
    ensure => present,
    shell  => '/bin/bash',
    home   => "/home/${username}"
  }

  Exec {
    path => '/bin/:/usr/bin'
  }

  # a majority of the relevant files are copied over
  # here. This makes it easy to add to existing configs
  # by modifying the single home directory in ytlaces.
  # this doesn't work well if sockets and fifos
  # exist under the root directory. to find them run:
  # $ find . -type s
  # $ find . -type p
  file {"/home/${username}/":
    ensure       => 'directory',
    recurse      => 'remote',
    recurselimit => 1,
    purge        => false,
    source       => 'puppet:///modules/ytlaces/home/',
    owner        => $username,
  }

  file {"/home/${username}/.config":
    ensure  => 'directory',
    recurse => true,
    purge   => false,
    source  => 'puppet:///modules/ytlaces/home/.config',
    owner   => $username,
  }

  file {"/home/${username}/bin":
    ensure  => 'directory',
    recurse => true,
    purge   => false,
    source  => 'puppet:///modules/ytlaces/home/bin',
    owner   => $username,
    mode    => '0755',
  }

  file {"/home/${username}/lib":
    ensure => 'directory',
    owner  => $username,
  }


  file {'.ssh':
    ensure => 'directory',
    path   => "/home/${username}/.ssh/",
    owner  => $username,
  }

  exec {"ssh-keygen -f id_rsa -t rsa -N ''":
    path    => '/usr/bin',
    creates => "/home/${username}/.ssh/id_rsa",
    user    => $username,
    cwd     => "/home/${username}/.ssh/",
  }

  file {'/etc/security/limits.conf':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/etc/security/limits.conf',
    owner  => 'root',
  }

  file {'/etc/systemd/user.conf':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/etc/systemd/user.conf',
    owner  => 'root',
  }

  # this is needed to clone certain repos, even outside
  # of programming
  package {'git':}
  package {'git-lfs':}

  include ytlaces::programs_universal
  class {'::ytlaces::sub':
    username => $username
  }
  class {'::ytlaces::terminal_config':
    username => $username
  }
  class {'::ytlaces::ui_awesome':
    username => $username
  }
  class {'::ytlaces::dropbox':
    username => $username
  }
  # conditional includes
  case $type {
    'desktop': {
      class {'::ytlaces::arch':
        username => $username
      }
      include ytlaces::desktop
      include ytlaces::network
      include ytlaces::virtualization
    }
    'laptop': {
      class {'::ytlaces::arch':
        username => $username
      }
      include ytlaces::laptop
      include ytlaces::network
    }
    'work': {
      class {'::ytlaces::work':
        username => $username
      }
    }
    'work_desktop': {
      class {'::ytlaces::arch':
        username => $username
      }
      include ytlaces::work_desktop
      include ytlaces::network
    }
  }
}
