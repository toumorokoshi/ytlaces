class ytlaces::bluetooth {
  package {'blueman':}
  package {'pulseaudio-bluetooth':}
  service { 'bluetooth.service':
    ensure   => 'running',
    provider => 'systemd',
    enable   => true,
  }
}
