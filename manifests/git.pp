class ytlaces::git (
  String $username = "tsutsumi"
){
  package {"git":}
  package {"git-lfs":}
  file {"/etc/bash_completion.d/git-completion.bash":
    ensure => "file",
    source => "https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash",
    owner => "root",
  }
}
