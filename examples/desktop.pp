class {'::ytlaces':
  type => 'desktop'

  # Using a GeForces TI 560, which is only
  # supported by legacy drivers now.
  package {"nvidia-390xx":}
  package {"nvidia-390xx-utils":}
}
