class ytlaces::ui_awesome {
  package {"awesome":}

  file {"/home/tsutsumi/.config/awesome/":
    ensure => 'directory',
    owner => "tsutsumi",
    recurse => "remote",
    source => "puppet:///modules/ytlaces/.config/awesome/",
  }

  vcsrepo { '/home/tsutsumi/.config/awesome/battery-widget':
    ensure   => present,
    provider => git,
    source => 'https://github.com/deficient/battery-widget.git',
    owner => 'tsutsumi',
  }

  vcsrepo { '/home/tsutsumi/.config/awesome/awesome-sharedtags':
    ensure   => present,
    provider => git,
    source => 'https://github.com/Drauthius/awesome-sharedtags.git',
    owner => 'tsutsumi',
  }
}
