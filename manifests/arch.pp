class ytlaces::arch(
  $username => 'tsutsumi',
) {
  file { "/etc/pacman.conf":
    ensure => "file",
    source => "puppet:///modules/ytlaces/etc/pacman.conf",
    owner => "root",
  }

  package {"openssh":}

  include ytlaces::audio
  include ytlaces::dropbox
  include ytlaces::fonts
  include ytlaces::input
  include ytlaces::programs
  class {'::ytlaces::programming_arch':
    username => $username
  }
  include ytlaces::secrets
  include ytlaces::termite
  include ytlaces::time
  include ytlaces::ui
  include ytlaces::ui_xmonad
  include ytlaces::vpn
}
