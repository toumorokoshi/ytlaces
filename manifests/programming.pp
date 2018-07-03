class ytlaces::programming {
  package {"atom":}
  package {"clojure":}
  package {"docker":}
  service {"docker":
    ensure => "running",
    enable => "true"
  }
  group {"docker":
    members => ["tsutsumi"]
  }
   package {"python":}
   # yaourt
   # package {"code":}
   package {"dotnet-runtime":}
   package {"dotnet-sdk":}
   package {"mono":}
   # this next part sets up nuget
   file {"/home/tsutsumi/lib/nuget.exe":
      ensure => "file",
      source => "https://dist.nuget.org/win-x86-commandline/v4.7.0/nuget.exe",
      owner => "tsutsumi",
  }
  file {"/home/tsutsumi/bin/nuget":
      ensure => "file",
      source => "puppet:///modules/ytlaces/home/bin/nuget",
      owner => "tsutsumi",
      mode => "0755"
  }

  package {"gdb":}
  file { '/home/tsutsumi/.gdbinit':
    ensure => 'file',
    source => "puppet:///modules/ytlaces/home/.gdbinit",
    mode => '0755',
  }

  file {"/home/tsutsumi/bin/flamegraph.pl":
      ensure => "file",
      source => "https://raw.githubusercontent.com/brendangregg/FlameGraph/master/flamegraph.pl",
      owner => "tsutsumi",
      mode => "0755"
  }
}
