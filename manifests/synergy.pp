# class to handle setting up synergy
# hard-coded to my desktop for now.
class ytlaces::synergy(
  String $username = 'tsutsumi',
) {
  file { '/etc/systemd/system/synergy.service':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/etc/systemd/user/synergy.service',
    owner  => $username
  }
}
