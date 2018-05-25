 class ytlaces::programming {
   package {"python":}
   package {"clojure":}
   package {"docker":}
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
}
