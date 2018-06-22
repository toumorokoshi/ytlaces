class ytlaces::ui {
  package {"noto-fonts":}
  package {"ttf-hack":}
  package {"xscreensaver":}
  package {"xorg-xfontsel":}
  package {"xorg-xlsfonts":}
  package {"xorg":}
  package {"lightdm":}
  package {"lightdm-gtk-greeter":}
  service {"lightdm":
    ensure => "running",
    enable => "true"
  }
  # file management
  package {"thunar":}
  # for thumbnails
  package {"tumbler":}
  package {"ffmpegthumbnailer":}
  # for tray
  package {"stalonetray":}
  file {"/home/tsutsumi/.stalonetrayrc":
   ensure => "file",
   source => "puppet:///modules/ytlaces/home/.stalonetrayrc",
   owner => "root",
   mode => "0644"
  }

}
