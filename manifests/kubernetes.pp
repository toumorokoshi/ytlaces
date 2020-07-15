class ytlaces::kubernetes(
  String $username = 'tsutsumi'
) {
  file {"/home/${username}/bin/minikube":
      ensure => 'file',
      source => 'https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64',
      owner  => $username,
      mode   => '0755'
  }
}
