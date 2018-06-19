class ytlaces::desktop {
  file {"/home/tsutsumi/.xprofile.desktop":
    ensure => "file",
    source => "puppet:///modules/ytlaces/.xprofile.desktop",
    owner => "tsutsumi"
  }
  # Using a GeForces TI 560, which is only
  # supported by legacy drivers now.
  package {"nvidia-390xx":}
  package {"nvidia-390xx-utils":}
}
