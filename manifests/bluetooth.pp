class ytlaces::bluetooth {
  package {'blueman':}
  service { 'bluetooth.service':
    ensure   => 'running',
    provider => 'systemd',
    enable   => true,
  }

  file {'/etc/bluetooth/main.conf':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/etc/bluetooth/main.conf',
  }
}
