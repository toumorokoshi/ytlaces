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
  file {"/etc/systemd/user/data.mount":
    ensure => "file",
    source => "puppet:///modules/ytlaces/desktop/data.mount",
    owner => "tsutsumi",
  }
}
