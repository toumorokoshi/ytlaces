class ytlaces::bluetooth {
  package {'bluez':}
  package {'bluez-utils':}
  package {'pulseaudio-bluetooth':}
  service { 'bluetooth.service':
    ensure => 'running',
    provider => 'systemd',
    enable => true,
  }
}
