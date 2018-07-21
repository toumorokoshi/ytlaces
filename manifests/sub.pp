class ytlaces::sub(
  String $username = 'tsutsumi'
) {
  file {"/home/$username/.ytlaces":
    ensure => 'directory',
    owner => $username,
  }

  vcsrepo {"/home/$username/.ytlaces/sub":
    ensure   => present,
    provider => git,
    source   => 'https://github.com/toumorokoshi/sub.git',
    owner => $username,
  }
}
