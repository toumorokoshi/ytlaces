 class ytlaces::laptop {
  package {'acpi':}

  file { '/usr/share/X11/xorg.conf.d/30-touchpad.conf':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/30-touchpad.conf',
    owner  => 'root'
  }

  file { '/usr/lib/systemd/system-sleep/local.sh':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/usr/lib/systemd/system-sleep/local.sh',
    owner  => 'root',
    mode   => '0755'
  }

  package {'acpid':}
  # installed by acpid
  service { 'acpid.service':
    ensure   => 'running',
    provider => 'systemd',
    enable   => true,
  }
  # volume controls acpi
  file { '/etc/acpi/events/vol-u':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/acpi/events/vol-u',
    owner  => 'root'
  }

  file { '/etc/acpi/events/vol-m':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/acpi/events/vol-m',
    owner  => 'root'
  }

  file { '/etc/acpi/events/vol-d':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/acpi/events/vol-d',
    owner  => 'root'
  }

  file { '/etc/acpi/handlers/':
    ensure => 'directory',
    owner  => 'root'
  }

  file { '/etc/acpi/handlers/bl':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/acpi/handlers/bl',
    owner  => 'root',
    mode   => '0755'
  }

  file { '/etc/acpi/events/bl-u':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/acpi/events/bl-u',
    owner  => 'root'
  }

  file { '/etc/acpi/events/bl-d':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/acpi/events/bl-d',
    owner  => 'root'
  }

  # touchscreen rotation
  file { '/opt/scripts/':
    ensure => 'directory',
    owner  => 'root'
  }

  file { '/opt/scripts/rotate_screen.py':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/scripts/rotate_screen.py',
    owner  => 'root'
  }

  file { '/etc/systemd/user/rotate-screen.service':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/laptop/rotate-screen.service',
    owner  => 'root'
  }

  # for now, have to enable by running
  # systemctl --user enable rotate-screen.service

  file { '/home/tsutsumi/.Xresources.d':
    ensure => 'directory',
    owner  => 'tsutsumi'
  }

  file {'/home/tsutsumi/.Xresources.d/laptop':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/.Xresources.laptop',
    owner  => 'tsutsumi'
  }

  file {'/home/tsutsumi/.Xresources.d/laptop_dock':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/.Xresources.laptop_dock',
    owner  => 'tsutsumi'
  }

  file {'/etc/systemd/logind.conf':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/laptop/etc/systemd/logind.conf',
  }

  vcsrepo { '/home/tsutsumi/.ytlaces/autorandr':
    ensure   => present,
    provider => git,
    source   => 'https://github.com/wertarbyte/autorandr',
    owner    => 'tsutsumi',
  }

  file { '/home/tsutsumi/bin/autorandr':
    ensure => 'link',
    target => '/home/tsutsumi/.ytlaces/autorandr/autorandr',
    mode   => '0755',
  }

  include ytlaces::thunderbolt
  include ytlaces::dock
}
