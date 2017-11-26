class ytlaces::xmonad {
  package {"xmonad-contrib":}
  package {"dzen2":}
  package {"conky":}

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
