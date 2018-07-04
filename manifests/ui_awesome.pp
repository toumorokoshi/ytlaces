class ytlaces::ui_awesome {
  package {"awesome":}

  file {"/home/tsutsumi/.config/awesome/":
    ensure => 'directory',
    owner => "tsutsumi"
  }

  file {"/home/tsutsumi/.config/awesome/rc.lua":
   ensure => "file",
   source => "puppet:///modules/ytlaces/.config/awesome/rc.lua",
   owner => "tsutsumi",
   mode => "0644"
  }

  vcsrepo { '/home/tsutsumi/.config/awesome/battery-widget':
    ensure   => present,
    provider => git,
    source => 'https://github.com/deficient/battery-widget.git',
    owner => 'tsutsumi',
  }
}
