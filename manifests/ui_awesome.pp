class ytlaces::ui_awesome(
  String $username = 'tsutsumi'
) {
  package {'awesome':}

  # packages used by awesome to manipulate things like screen
  # brightness
  package {'brightnessctl':}

  vcsrepo {"/home/${username}/.config/awesome/battery-widget":
    ensure   => present,
    provider => git,
    source   => 'https://github.com/deficient/battery-widget.git',
    owner    => $username,
  }
}
