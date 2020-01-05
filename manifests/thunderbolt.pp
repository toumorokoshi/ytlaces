# configuration to enable thunderbolt
class ytlaces::thunderbolt {
  package {'bolt':}
  file {'/etc/udev/rules.d/99-removable.rules':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/etc/udev/rules.d/99-removable.rules',
  }
}
