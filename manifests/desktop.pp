class ytlaces::desktop {
  file {"/home/tsutsumi/.xinitrc.desktop":
    ensure => "file",
    source => "puppet:///modules/ytlaces/.xinitrc.desktop",
    owner => "tsutsumi"
  }
}
