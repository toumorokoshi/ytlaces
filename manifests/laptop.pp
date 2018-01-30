 class ytlaces::laptop {
  package {"acpi":}

  file { "/usr/share/X11/xorg.conf.d/30-touchpad.conf":
    ensure => "file",
    source => "puppet:///modules/ytlaces/30-touchpad.conf",
    owner => "root"
  }

  package {"acpid":}
  # installed by acpid
  service { "acpid.service":
    provider => "systemd",
    ensure => "running",
    enable => "true",
  }
  # volume controls acpi
  file { "/etc/acpi/events/vol-u":
    ensure => "file",
    source => "puppet:///modules/ytlaces/acpi/events/vol-u",
    owner => "root"
  }

  file { "/etc/acpi/events/vol-m":
    ensure => "file",
    source => "puppet:///modules/ytlaces/acpi/events/vol-m",
    owner => "root"
  }

  file { "/etc/acpi/events/vol-d":
    ensure => "file",
    source => "puppet:///modules/ytlaces/acpi/events/vol-d",
    owner => "root"
  }

  file { "/etc/acpi/handlers/":
    ensure => "directory",
    owner => "root"
  }

  file { "/etc/acpi/handlers/bl":
    ensure => "file",
    source => "puppet:///modules/ytlaces/acpi/handlers/bl",
    owner => "root",
    source_permissions => "use"
  }

  file { "/etc/acpi/events/bl-u":
    ensure => "file",
    source => "puppet:///modules/ytlaces/acpi/events/bl-u",
    owner => "root"
  }

  file { "/etc/acpi/events/bl-d":
    ensure => "file",
    source => "puppet:///modules/ytlaces/acpi/events/bl-d",
    owner => "root"
  }

  # touchscreen rotation
  file { "/opt/scripts/":
    ensure => "directory",
    owner => "root"
  }

  file { "/opt/scripts/rotate_screen.py":
    ensure => "file",
    source => "puppet:///modules/ytlaces/scripts/rotate_screen.py",
    owner => "root"
  }

  file { "/etc/systemd/user/rotate-screen.service":
    ensure => "file",
    source => "puppet:///modules/ytlaces/laptop/rotate-screen.service",
    owner => "root"
  }

  # for now, have to enable by running
  # systemctl --user enable rotate-screen.service

  file { "/home/tsutsumi/.Xresources.d":
    ensure => "directory",
    owner => "tsutsumi"
  }

  file {"/home/tsutsumi/.Xresources.d/laptop":
    ensure => "file",
    source => "puppet:///modules/ytlaces/.Xresources.laptop",
    owner => "tsutsumi"
  }
}
