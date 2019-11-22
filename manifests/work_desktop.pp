class ytlaces::work_desktop(
  String $username = 'yusuket'
) {
  file { "/home/${username}/.Xresources.d":
    ensure => 'directory',
    owner  => $username,
  }

  file {"/home/${username}/.xprofile.work":
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/.xprofile.work',
    owner  => $username
  }

  file {'/etc/X11/xorg.conf.d/20-intel.conf':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/work/etc/X11/xorg.conf.d/20-intel.conf',
  }
}
