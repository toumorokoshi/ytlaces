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

  file {"/home/${username}/.ytlaces/packages/cookbook":
    ensure => "directory",
    owner  => $username,
  }

  exec {"unpack cookbook":
    command     => "curl -L 'https://github.com/toumorokoshi/cookbook/releases/download/v0.1.1/cookbook.tar.gz' | tar -xzvf",
    cwd         => "/home/${username}/.ytlaces/packages/cookbook",
    refreshonly => true,
    user => $username,
  }

  file {"/home/${username}/.ytlaces/cookbook":
    ensure  => 'directory',
    recurse => true,
    purge   => true,
    source  => 'puppet:///modules/ytlaces/cookbook',
    source_permissions => 'use',
    owner   => $username,
  }


}
