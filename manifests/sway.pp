# sway
class ytlaces::sway(
) {
  package {'sway':}
  # for IME support
  package {'fcitx5':}
  # Japanese IME
  package {'fcitx5-mozc':}
  # TODO: install swaync for notifications

  # add GDM desktop session
  file {'/usr/share/wayland-sessions/sway.desktop':
      ensure => 'file',
      source => 'puppet:///modules/ytlaces/usr/share/wayland-sessions/sway.desktop',
  }
}
