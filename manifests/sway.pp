class {'::sway':
  # manual configuration
  # - configure fcitx with fcitx5-config.
  type => 'sway',
  username => 'tsutsumi'

  # for IME support
  package {'fcitx5':}
  # Japanese IME
  package {'fcitx5-mozc':}
}
