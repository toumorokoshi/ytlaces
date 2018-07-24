class ytlaces::ui_awesome_work {

  file {"/usr/share/xsessions/awesome-gnome.desktop":
    ensure => "file",
    source => "puppet:///modules/ytlaces/work/usr/share/xsessions/awesome-gnome.desktop",
  }

  file {"/usr/share/gnome-session/sessions/awesome.session":
    ensure => "file",
    source => "puppet:///modules/ytlaces/work/usr/share/gnome-session/sessions/awesome.session",
  }

  file {"/usr/share/applications/awesome.desktop":
    ensure => "file",
    source => "puppet:///modules/ytlaces/work/usr/share/applications/awesome.desktop",
  }

  package {"gnome-settings-daemon":}
}
