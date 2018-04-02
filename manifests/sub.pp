class ytlaces::sub {
  file {"/home/tsutsumi/.ytlaces":
    ensure => 'directory',
    owner => "tsutsumi"
  }

  vcsrepo { '/home/tsutsumi/.ytlaces/sub':
    ensure   => present,
    provider => git,
    source   => 'https://github.com/toumorokoshi/sub.git',
    owner => 'tsutsumi',
  }
}
