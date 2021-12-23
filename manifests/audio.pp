class ytlaces::audio {
  package {'alsa-utils':}
  package {'pulseaudio':}
  package {'pavucontrol':}
  # used to control media buttons
  package {'playerctl': }
}
