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
}
