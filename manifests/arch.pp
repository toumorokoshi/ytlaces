class ytlaces::arch(
  String $username = 'tsutsumi',
) {
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

  # needed for building aur packages
  package {'binutils':}
  package {'gcc':}

  include ytlaces::audio
  include ytlaces::dropbox
  include ytlaces::fonts
  include ytlaces::input
  include ytlaces::programs
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
