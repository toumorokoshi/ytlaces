class ytlaces::vpn {
  # enables the international characters (e.g. japanese)
  package {"openconnect":}
  file {"/etc/NetworkManager/dispatcher.d/handle_vpn":
   ensure => "file",
   source => "puppet:///modules/ytlaces/etc/NetworkManager/dispatcher.d/handle_vpn",
   owner => "root",
   mode => "0755"
  }

  file {"/etc/vpnc/connect.d/":
   ensure => 'directory',
  }

  file {"/etc/vpnc/connect.d/write_gateway_file":
   ensure => "file",
   source => "puppet:///modules/ytlaces/etc/vpnc/connect.d/write_gateway_file",
   owner => "root",
   mode => "0755"
  }

  file {"/etc/vpnc/post-disconnect.d/":
   ensure => 'directory',
  }

  file {"/etc/vpnc/post-disconnect.d/delete_gateway_file":
   ensure => "file",
   source => "puppet:///modules/ytlaces/etc/vpnc/post-disconnect.d/delete_gateway_file",
   owner => "root",
   mode => "0755"
  }
  
  # not using nmgui at the moment,
  # the command line is a bit more convenient.
  # package {"stalonetray":}
  # package {"network-manager-applet":}

  # file {"/home/tsutsumi/bin/":
  #   ensure => 'directory',
  #   owner => "tsutsumi"
  # }
  # file {"/home/tsutsumi/bin/nmgui/":
  #   ensure => "file",
  #   source => "puppet:///modules/ytlaces/home/bin/nmgui",
  #   owner => "tsutsumi",
  #   mode => "0755"
  # }
}
