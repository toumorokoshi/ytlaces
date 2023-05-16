# insync installs insync packages
class ytlaces::insync(
  String $username = 'tsutsumi',
) {
  package {'insync':}
  # insync started as a service allows the tray
  # icon to show
  service { "insync@${username}.service":
    ensure   => 'running',
    provider => 'systemd',
    enable   => true,
  }
}
