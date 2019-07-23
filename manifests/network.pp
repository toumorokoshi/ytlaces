class ytlaces::network {
  package {'networkmanager':}
  service {'NetworkManager':
    ensure => 'running',
    enable => true
  }

  service {'systemd-resolved':
    ensure => 'running',
    enable => true
  }
  # for some reason systemd-resolve doesn't add the 
  # symlink, so we need to. or else systemd-resolve
  # won't be the source of truth for vpn.
  file {'/etc/resolv.conf':
    ensure => 'link',
    target => '/var/run/systemd/resolve/resolv.conf',
  }
  # to disable multicast dns
  file {'/etc/systemd/resolved.conf':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/etc/systemd/resolved.conf',
  }
  # to use the standard dns database over 
  # the systemd-resolver.
  file {'/etc/nsswitch.conf':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/etc/nsswitch.conf',
  }
  file {'/etc/resolvconf.conf':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/etc/resolvconf.conf',
  }

  file {'/etc/vpnc/connect.d/parse_cisco_dns':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/etc/vpnc/connect.d/parse_cisco_dns',
    mode   => '0755'
  }

  file {'/lib/sysctl.d/09-disable-ipv6.conf':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/lib/sysctl.d/09-disable-ipv6.conf',
    mode   => '0644'
  }
}
