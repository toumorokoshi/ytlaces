# a collection of files to help make docking more seamless
class ytlaces::dock {
  # to enable the script to copy and remove laptop dpi settings
  file {'/home/tsutsumi/.Xresources.d/laptop.bak':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/.Xresources.laptop',
    owner  => 'tsutsumi'
  }
}
