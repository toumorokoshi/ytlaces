class ytlaces::dropbox(
  String $username = 'tsutsumi',
) {
  # can't get it working due to yaourt needing to run
  # package {"dropbox":}
  # the dropbox-dist directory being writable
  # results in an infinite update loop for linux
  # machines. To prevent this, making the directory
  # read-only.
  file {"/home/$username/.dropbox-dist":
    ensure => "directory",
    owner => $username,
    mode => "0444"
  }
}
