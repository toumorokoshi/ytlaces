class ytlaces::terminal_config(
  String $username = 'tsutsumi'
){
  file {"/home/${username}/.ytlaces/init":
    ensure => 'file',
    source => 'puppet:///modules/ytlaces/init',
    owner  => $username,
  }

  file {"/home/${username}/.tmux.conf":
   ensure => 'file',
   source => 'puppet:///modules/ytlaces/home/.tmux.conf',
   owner  => $username,
  }
}
