class ytlaces::sub(
  String $username = 'tsutsumi'
) {
  file {"/home/${username}/.ytlaces":
    ensure => 'directory',
    owner  => $username,
  }

  file {"/home/${username}/.ytlaces/packages":
    ensure => 'directory',
    owner  => $username,
  }

  vcsrepo {"/home/${username}/.ytlaces/sub":
    ensure   => present,
    provider => git,
    source   => 'https://github.com/toumorokoshi/sub.git',
    owner    => $username,
  }

  # install tome executable
  exec {'install tome':
    command     => "curl -L 'https://github.com/toumorokoshi/tome/releases/download/v0.3.0/tome-linux' > ~/bin/tome && chmod 0755 ~/bin/tome",
    user        => $username,
    refreshonly =>  true,
  }

  # install tome scripts
  file {"/home/${username}/.ytlaces/cookbook":
    ensure             => 'directory',
    recurse            => true,
    purge              => true,
    source             => 'puppet:///modules/ytlaces/cookbook',
    source_permissions => 'use',
    owner              => $username,
  }
}
