class laces {
  user { "tsutsumi":
    ensure => present,
    shell => "/bin/bash",
    home => "/home/tsutsumi"
  }

  file { "xresources":
    path => "/home/tsutsumi/.Xresources",
    ensure => "file",
    source => "puppet:///modules/laces/.Xresources"
  }
}

class {"laces":}
