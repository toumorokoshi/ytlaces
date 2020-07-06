class ytlaces::virtualization  {
  file {'/etc/libvirt/qemu.conf':
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/virtualization/qemu.conf',
  }
}
