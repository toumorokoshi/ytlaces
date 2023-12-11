class ytlaces::sub(
  String $username = 'tsutsumi'
) {
  file {"/home/${username}/.ytlaces":
    ensure => 'directory',
    owner  => $username,
  }

  file {"/home/${username}/.ytlaces/packages":
    ensure => 'directory',
    owner  => $username,
  }

  # install tome executable
  exec {'install tome':
    command => "curl -L 'https://github.com/toumorokoshi/tome/releases/download/v0.11.1/tome-linux_amd64' > /home/$username/bin/tome && chmod 0755 /home/$username/bin/tome",
    user    => $username,
  }
}
