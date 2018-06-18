class ytlaces::network {
  package {"networkmanager":}
  service {"NetworkManager":
    ensure => "running",
    enable => "true"
  }
}
