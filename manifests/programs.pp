class ytlaces::programs(
  String $username = 'tsutsumi'
) {
  # programs to install
  # uses the AUR + yaourt.
  # package {"write-stylus":}
  package {'hexchat':}
  package {'fzf':}

  exec {'/home/tsutsumi/bin/pacman-static':
    command => "curl -L 'https://pkgbuild.com/~eschwartz/pacman-static' > ~/bin/pacman-static && chmod 0755 ~/bin/pacman-static",
    user    => $username,
  }
}
