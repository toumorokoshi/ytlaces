class ytlaces::virtualization  {
  package {"ovmf":}

  file {"/etc/libvirt/qemu.conf":
    source => "puppet:///modules/ytlaces/virtualization/qemu.conf",
    ensure => 'file',
  }
}
