class ytlaces::audio {
  package {'alsa-utils':}
  package {'pulseaudio':}
  package {'pavucontrol':}
  # used to control media buttons
  package {'playerctl': }
  # not clear if this is just for arch or not yet.
  # install some pulseaudio plugins
  # pulseaudio-alsa ensures applications that connect directly to
  # alsa (wine, ruffle) use pulseaudio instead.
  package {'pulseaudio-alsa':}
  # install 32bit variant binaries for steam / 32bit app support.
  package {'lib32-libpulse':}
  package {'lib32-alsa-plugins':}

}
