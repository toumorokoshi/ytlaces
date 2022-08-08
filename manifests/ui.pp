class ytlaces::ui {
  # for full unicode support, including japanese characters
  package {'noto-fonts':}
  package {'noto-fonts-cjk':}
  package {'noto-fonts-emoji':}
  package {'ttf-hack':}
  package {'xorg-xfontsel':}
  package {'xorg-xlsfonts':}
  package {'xorg':}
  package {'lightdm':}
  package {'lightdm-gtk-greeter':}
  service {'lightdm':
    ensure => 'running',
    enable => 'true'
  }
  # file management
  package {'nomacs':} # image viewer
  package {'qt5-imageformats':} # view webp in nomacs
  # this helps browsers such as chrome, which use xdg-desktop-portal.
  # choosing KDE-based technologies in particular since some apps (Chrome)
  # tend to hard-code support for specific desktop environments, and the
  # technologies need to match.
  #
  # if the apps honor layers of abstraction (like xdg-mime), then we can
  # use those.
  package {'dolphin':}  # kde file manager
  # if you don't install this first, xdg-desktop-portal seems to force
  # xdg-desktop-portal-gnome
  package {'xdg-desktop-portal-kde':}
  package {'xdg-desktop-portal':}
  package {'gvfs':}
  # for thumbnails
  package {'tumbler':}
  package {'ffmpegthumbnailer':}
  # for screenshots
  package {'scrot':}
  package {'xclip':}
}
