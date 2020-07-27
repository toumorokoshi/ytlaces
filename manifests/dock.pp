# a collection of files to help make docking more seamless
class ytlaces::dock {
  file { '/etc/udev/rules.d/thunderbolt3-dock.rules':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/laptop/etc/udev/rules.d/thunderbolt3-dock.rules',
  }

  # to enable the script to copy and remove laptop dpi settings
  file {'/home/tsutsumi/.Xresources.d/laptop.bak':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/.Xresources.laptop',
    owner  => 'tsutsumi'
  }

  file { '/opt/ytlaces/dock.sh':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/laptop/opt/ytlaces/dock.sh',
    mode   => '0755',
  }
}
