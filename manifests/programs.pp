class ytlaces::programs {
  # programs to install
  # uses the AUR + yaourt.
  # package {"write-stylus":}
  package {"firefox":}
  package {"hexchat":}
  package {"patch":}
  package {"tree":}
  package {"tmux":}

  file {"/home/tsutsumi/bin/pacman-static":
    ensure => "file",
    source => "https://pkgbuild.com/~eschwartz/pacman-static",
    owner => "tsutsumi",
    mode => "0755",
  }
}
