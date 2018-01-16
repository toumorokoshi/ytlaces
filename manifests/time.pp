class ytlaces::time {
  package {"ntp":}

  service {"ntpd":
    ensure => "running",
    enable => true,
  }
  # there shouldn't be any more work than this,
  # but the preferred settings are:
  # hw clock: UTC (that's how Windows likes it)
  # /etc/adjusttime utc
}
