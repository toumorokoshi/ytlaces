class ytlaces::arch(
  String $username = 'tsutsumi',
) {

  # set default shell to zsh
  user { $username:
    ensure => present,
    shell  => '/bin/zsh',
    home   => "/home/${username}"
  }

  file { '/etc/pacman.conf':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/etc/pacman.conf',
    owner  => 'root',
  }

  # we don't like .local, so let's switch
  # that to .avahi.
  file { '/etc/avahi/avahi-daemon.conf':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/etc/avahi/avahi-daemon.conf',
    owner  => 'root',
  }

  # arch default terminal
  package {'alacritty':}
  # needed for building aur packages
  package {'binutils':}
  package {'base-devel':}
  package {'gcc':}
  package {'go':}

  # arch linux provides this package
  package {'openssh':}

  include ytlaces::audio
  include ytlaces::dropbox
  include ytlaces::fonts
  include ytlaces::printing
  class {'::ytlaces::programs':
    username => $username
  }
  class {'::ytlaces::programming_arch':
    username => $username
  }
  include ytlaces::secrets
  include ytlaces::terminal
  include ytlaces::time
  include ytlaces::ui
  # include ytlaces::ui_xmonad
  include ytlaces::vpn
  include ytlaces::yubikey
}
