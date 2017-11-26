class ytlaces::xmonad {
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

  /* exec {"xmonad --recompile":
    path => "/usr/bin",
    user => "tsutsumi",
  } */
}
