class ytlaces::screensaver(
  String $username = 'tsutsumi'
) {
  package {'xscreensaver':}
  file { '/etc/systemd/system/lock@.service':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/etc/systemd/system/lock@.service',
  }
  service {"lock@${username}.service":
    enable => 'true',
  }
}
