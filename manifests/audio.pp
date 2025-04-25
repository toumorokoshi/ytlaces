class ytlaces::audio {
  package {'alsa-utils':}
  # using pipewire rather than pulseaudio,
  # as it seems pipewire is the sucessor.
  package {'pipewire':}
  package {'pipewire-pulse':}
  package {'pavucontrol':}
  # used to control media buttons
  package {'playerctl': }
  # package {'lib32-libpulse':}
  # package {'lib32-alsa-plugins':}
  # I've had issues with the pulseaudio-media-session package,
  # with The p15v3 Thinkpad not supporting audio using it.
  #
  # Wireplumber is the recommended solution anyway.
  package {'wireplumber':}
}
