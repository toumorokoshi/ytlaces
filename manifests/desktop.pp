class ytlaces::desktop {
  file {'/home/tsutsumi/.xprofile.desktop':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/.xprofile.desktop',
    owner  => 'tsutsumi'
  }
  # Using a GeForces TI 560, which is only
  # supported by legacy drivers now.
  package {'nvidia-390xx':}
  package {'nvidia-390xx-utils':}
  file {'/usr/lib/systemd/system/mnt-data.mount':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/desktop/mnt-data.mount',
    owner  => 'tsutsumi',
  }
  file {'/etc/default/grub':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/desktop/etc/default/grub',
  }
  file {'/etc/fstab':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/desktop/etc/fstab',
  }
  file {'/etc/exports':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/desktop/etc/exports',
  }
  # nfs
  file {'/srv/nfs':
    ensure => 'directory',
  }
  package {'nfs-utils':}
  # start nfs server
  service { 'nfs-server.service':
    ensure   => 'running',
    provider => 'systemd',
    enable   => true,
  }
}
