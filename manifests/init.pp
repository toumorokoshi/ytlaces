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
    recurselimit => 10,
    purge        => false,
    source       => 'puppet:///modules/ytlaces/home/',
    owner        => $username,
  }

  package {'rsync':}
  # have to break down config into subdirectories due to some applications
  # putting sockets in the config directory.
  # file {"/home/${username}/.config":
  #   ensure  => 'directory',
  #   recurse => true,
  #   purge   => false,
  #   source  => 'puppet:///modules/ytlaces/home/.config',
  #   owner   => $username,
  #   # sometimes new sockets may pop up, which have to be ignored.
  #   # find them via `tree --inodes -F | grep =`
  #   ignore  => '{*.sock*,*SingletonSocket*}'
  # }
  exec {'sync-config':
    command => "rsync -rav ./files/home/.config/ /home/${username}/.config/",
    user    => $username
  }

  exec {'sync-ytlaces':
    command => "rsync -rav ./files/home/.ytlaces/ /home/${username}/.ytlaces/",
    user    => $username
  }


  file {"/home/${username}/bin":
    ensure  => 'directory',
    recurse => true,
    purge   => false,
    source  => 'puppet:///modules/ytlaces/home/bin',
    owner   => $username,
    mode    => '0755',
  }

  file {"/home/${username}/bin/mem-xrandr":
      ensure => 'file',
      source => 'https://raw.githubusercontent.com/toumorokoshi/mem-xrandr/main/mem-xrandr',
      owner  => $username,
      mode   => '0755'
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

  # preferred editor
  package {'vim':}

# do this manually.
#  exec {"ssh-keygen -f id_rsa -t rsa -N ''":
#    path    => '/usr/bin',
#    creates => "/home/${username}/.ssh/id_rsa",
#    user    => $username,
#    cwd     => "/home/${username}/.ssh/",
#  }

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

  include ytlaces::audio
  include ytlaces::input
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
  class {'::ytlaces::screensaver':
    username => $username
  }
  # disabled since I can't install
  # insync via puppet.
  class {'::ytlaces::insync':
    username => $username
  }
  class {'::ytlaces::kubernetes':
    username => $username
  }

  # rules to get elecom trackball to scroll with
  # the trackball.
  file {'/etc/X11/xorg.conf.d/40-elecom-trackball.conf':
      ensure => 'file',
      source => 'puppet:///modules/ytlaces/etc/X11/xorg.conf.d/40-elecom-trackball.conf',
  }
  include ytlaces::sway

  # conditional includes
  case $type {
    'desktop': {
      class {'::ytlaces::arch':
        username => $username
      }
      include ytlaces::desktop
      include ytlaces::network
      include ytlaces::synergy
      include ytlaces::virtualization
      # arch-only package
      package {'pipewire-alsa':}
    }
    'laptop': {
      class {'::ytlaces::arch':
        username => $username
      }
      include ytlaces::laptop
      include ytlaces::network
      # include ytlaces::bluetooth
      include ytlaces::wine
      # install swaync for notifications
    }

    'work': {
      file {"/home/${username}/.xprofile.work":
        ensure => 'file',
        source => 'puppet:///modules/ytlaces/.xprofile.work',
        owner  => $username
      }

      # In ubuntu 20.04, the brightnessctl package does not seem to
      # install the rules for us.
      file {'/etc/udev/rules.d/90-brightnessctl.rules':
        ensure => 'file',
        source => 'puppet:///modules/ytlaces/etc/udev/rules.d/90-brightnessctl.rules',
      }

      package {'scrot':}
      package {'xclip':}
      package {'pulseaudio-utils':}
      # for shell completion improvement
      package {'fzf':}
      package {'redshift-gtk':}
      # sync time
      package {'systemd-timesyncd':}
    }
  }
}
