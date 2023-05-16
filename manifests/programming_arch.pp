class ytlaces::programming_arch(
  String $username = 'tsutsumi'
) {
  package {'clojure':}
  # for python vscode symbols
  package {'ctags':}
  # docker configs
  package {'podman':}
  # debugging linux
  package {'sysstat':}
  # python
  package {'python':}
  package {'pyenv':}
  # yaourt
  package {'visual-studio-code-bin':}
  package {'dotnet-runtime':}
  package {'dotnet-sdk':}
  package {'mono':}
  # this next part sets up nuget
  file {"/home/${username}/lib/nuget.exe":
      ensure => 'file',
      source => 'https://dist.nuget.org/win-x86-commandline/v4.7.0/nuget.exe',
      owner  => $username,
  }
  file {"/home/${username}/bin/nuget":
      ensure => 'file',
      source => 'puppet:///modules/ytlaces/home/bin/nuget',
      owner  => $username,
      mode   => '0755'
  }

  package {'gdb':}
  file {"/home/${username}/.gdbinit":
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/home/.gdbinit',
    mode   => '0755',
    owner  => $username,
  }

  file {"/home/${username}/bin/flamegraph.pl":
      ensure => 'file',
      source => 'https://raw.githubusercontent.com/brendangregg/FlameGraph/master/flamegraph.pl',
      owner  => $username,
      mode   => '0755'
  }
}
