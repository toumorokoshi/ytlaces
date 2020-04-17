class ytlaces::printing {
  package {'cups':}
  package {'system-config-printer':}
  service {'org.cups.cupsd.service':
    ensure => 'running',
    enable => true
  }
  # hp drivers, my home printer. From the AUR.
  package {'hplip':}
}
