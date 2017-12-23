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
}
