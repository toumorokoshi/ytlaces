class ytlaces::ui_xmonad {
  package {"xmonad-contrib":}
  # status bar
  package {"dzen2":}
  package {"conky":}
  # app launch bar
  package {"dmenu":}

  file {"/home/tsutsumi/.xmonad":
    ensure => "directory",
    recurse => true,
    purge => false,
    source => "puppet:///modules/ytlaces/home/.xmonad",
    owner => "tsutsumi",
  }


  exec {"xmonad --recompile":
    path => ["/usr/bin"],
    user => "tsutsumi",
    environment => ["HOME=/home/tsutsumi"]
  }
}
