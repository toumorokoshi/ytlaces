class ytlaces::work(
  String $username = 'yusuket',
) {

  file {"/home/$username/.xprofile.work":
    ensure => "file",
    source => "puppet:///modules/ytlaces/.xprofile.work",
    owner => $username
  }
}
