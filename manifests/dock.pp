# a collection of files to help make docking more seamless
class ytlaces::dock {
  file { '/etc/udev/rules.d/thunderbolt3-dock.rules':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/laptop/etc/udev/rules.d/thunderbolt3-dock.rules',
  }

  file { '/opt/ytlaces/dock.sh':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/laptop/opt/ytlaces/dock.sh',
    mode   => '0755',
  }
}
