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

  # install tome executable
  exec {'install tome':
    command => "curl -L 'https://github.com/toumorokoshi/tome/releases/download/v0.7.5/tome-linux' > ~/bin/tome && chmod 0755 ~/bin/tome",
    user    => $username,
  }

  # install tome scripts
  file {"/home/${username}/.ytlaces/cookbook":
    ensure  => 'directory',
    recurse => true,
    purge   => true,
    source  => 'puppet:///modules/ytlaces/cookbook',
    owner   => $username,
    mode    =>  '0755'
  }
}
