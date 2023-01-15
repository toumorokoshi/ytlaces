class ytlaces::arch(
  String $username = 'tsutsumi',
) {

  # set default shell to zsh
  user { $username:
    ensure     => present,
    shell      => '/bin/zsh',
    home       => "/home/${username}",
    membership => 'minimum',
    groups     => [
      # enables access to input devices for udev,
      # which enables reading things like tablet mode
      # toggling.
      'input',
    ]
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
  include ytlaces::time
  include ytlaces::ui
  include ytlaces::vpn
  include ytlaces::yubikey
}
