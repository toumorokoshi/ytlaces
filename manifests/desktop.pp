class ytlaces::desktop {
  file {"/home/tsutsumi/.xprofile.desktop":
    ensure => "file",
    source => "puppet:///modules/ytlaces/.xprofile.desktop",
    owner => "tsutsumi"
  }
}
