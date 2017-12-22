 class ytlaces::laptop {
  package {"acpi":}

  file { "/usr/share/X11/xorg.conf.d/30-touchpad.conf":
    ensure => "file",
    source => "puppet:///modules/ytlaces/30-touchpad.conf",
    owner => "root"
  }
}
