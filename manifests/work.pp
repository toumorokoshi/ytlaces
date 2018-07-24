class ytlaces::work(
  String $username = 'yusuket',
) {
  file { "/home/$username/.Xresources.d":
    ensure => "directory",
    owner => $username,
  }

  file {"/home/$username/.Xresources.d/laptop":
    ensure => "file",
    source => "puppet:///modules/ytlaces/.Xresources.laptop",
    owner => $username
  }

  file {"/home/$username/.xprofile.work":
    ensure => "file",
    source => "puppet:///modules/ytlaces/.xprofile.work",
    owner => $username
  }

  include ytlaces::ui_awesome_work
}
