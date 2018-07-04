class ytlaces::ui_xmonad {
  package {"xmonad-contrib":}
  # status bar
  package {"dzen2":}
  package {"conky":}
  # app launch bar
  package {"dmenu":}

  file {".xmonad":
    path => '/home/tsutsumi/.xmonad',
    ensure => "directory",
    recurse => "remote",
    source => "puppet:///modules/ytlaces/xmonad",
    owner => "tsutsumi"
  }

  # for tray
  package {"stalonetray":}
  file {"/home/tsutsumi/.stalonetrayrc":
   ensure => "file",
   source => "puppet:///modules/ytlaces/home/.stalonetrayrc",
   owner => "root",
   mode => "0644"
  }

  /* exec {"xmonad --recompile":
    path => "/usr/bin",
    user => "tsutsumi",
  } */
}
