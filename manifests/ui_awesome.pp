class ytlaces::ui_awesome(
  String $username = 'tsutsumi'
) {
  package {'awesome':}
  package {'alacritty':}

  vcsrepo {"/home/${username}/.config/awesome/battery-widget":
    ensure   => present,
    provider => git,
    source   => 'https://github.com/deficient/battery-widget.git',
    owner    => $username,
  }
}
