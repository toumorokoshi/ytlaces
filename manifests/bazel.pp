class ytlaces::bazel(
  String $username = 'tsutsumi'
) {

  # install bazelisk executable
  exec {'install tome':
    command => "curl -L 'https://github.com/bazelbuild/bazelisk/releases/download/v1.19.0/bazelisk-linux-amd64' > /home/$username/bin/bazelisk && chmod 0755 /home/$username/bin/bazelisk",
    user    => $username,
  }
}
