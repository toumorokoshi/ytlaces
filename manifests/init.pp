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
class ytlaces (String $type = 'desktop') {
  user { "tsutsumi":
    ensure => present,
    shell => "/bin/bash",
    home => "/home/tsutsumi"
  }

  file { "xresources":
    path => "/home/tsutsumi/.Xresources",
    ensure => "file",
    source => "puppet:///modules/ytlaces/.Xresources",
    owner => "tsutsumi"
  }

  file {"/home/tsutsumi/.profile":
    ensure => "file",
    source => "puppet:///modules/ytlaces/.profile",
    owner => "tsutsumi"
  }

  file {"/home/tsutsumi/.xprofile":
    ensure => "file",
    source => "puppet:///modules/ytlaces/.xprofile",
    owner => "tsutsumi"
  }

  file { "gitconfig":
    path => "/home/tsutsumi/.gitconfig",
    ensure => "file",
    source => "puppet:///modules/ytlaces/.gitconfig",
    owner => "tsutsumi"
  }

  file { "/home/tsutsumi/.gitconfig.zillow":
    ensure => "file",
    source => "puppet:///modules/ytlaces/.gitconfig.zillow",
    owner => "tsutsumi"
  }

  file { "/home/tsutsumi/.gitignore_global":
    ensure => "file",
    source => "puppet:///modules/ytlaces/.gitignore",
    owner => "tsutsumi"
  }

  file { "/etc/pacman.conf":
    ensure => "file",
    source => "puppet:///modules/ytlaces/etc/pacman.conf",
    owner => "root",
  }

  package {"openssh":}

  file {".ssh":
    path => '/home/tsutsumi/.ssh/',
    ensure => 'directory',
    owner => "tsutsumi"
  }

  file {"/home/tsutsumi/lib":
    ensure => 'directory',
    owner => "tsutsumi"
  }

  file {"/home/tsutsumi/bin":
    ensure => 'directory',
    owner => "tsutsumi"
  }

  file {"/home/tsutsumi/.config":
    ensure => 'directory',
    owner => "tsutsumi"
  }

  exec {"ssh-keygen -f id_rsa -t rsa -N ''":
    path => "/usr/bin",
    creates => "/home/tsutsumi/.ssh/id_rsa.pub",
    user => "tsutsumi",
    cwd => "/home/tsutsumi/.ssh/"
  }

  file {"/etc/security/limits.conf":
    ensure => "file",
    source => "puppet:///modules/ytlaces/etc/security/limits.conf",
    owner => "root",
  }

  file {"/etc/systemd/user.conf":
    ensure => "file",
    source => "puppet:///modules/ytlaces/etc/systemd/user.conf",
    owner => "root",
  }

  # this is needed to clone certain repos, even outside
  # of programming
  package {"git":}
  package {"git-lfs":}

  include ytlaces::audio
  include ytlaces::dropbox
  include ytlaces::fonts
  include ytlaces::input
  include ytlaces::programming
  include ytlaces::programs
  include ytlaces::secrets
  include ytlaces::sub
  include ytlaces::terminal
  include ytlaces::terminal_config
  include ytlaces::time
  include ytlaces::ui
  include ytlaces::ui_xmonad
  include ytlaces::ui_awesome
  include ytlaces::vpn

  # conditional includes
  case $type {
    'desktop': {
      include ytlaces::desktop
      include ytlaces::virtualization
    }
    'laptop': {
      include ytlaces::laptop
    }
  }
}
