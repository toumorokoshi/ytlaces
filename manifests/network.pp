class ytlaces::network {
  package {"networkmanager":}
  service {"NetworkManager":
    ensure => "running",
    enable => "true"
  }
  file {"/etc/resolvconf.conf":
    ensure => "file",
    source => "puppet:///modules/ytlaces/etc/resolvconf.conf",
  }
}
