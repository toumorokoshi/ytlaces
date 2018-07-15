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
  package {"gvfs":}
  # for thumbnails
  package {"tumbler":}
  package {"ffmpegthumbnailer":}
}
