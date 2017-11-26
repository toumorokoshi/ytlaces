class ytlaces::xmonad {
  package {"xmonad-contrib":}

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
