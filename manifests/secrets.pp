class ytlaces::secrets {
  # libsecret seems to be the only thing required
  package {"libsecret":}
  package {"gnome-keyring":}
}
