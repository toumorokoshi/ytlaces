class ytlaces::terminal_config(
  String $username = 'tsutsumi'
){
  file {"/home/${username}/.ytlaces/rc.d":
    ensure             => 'directory',
    recurse            => true,
    purge              => true,
    source             => 'puppet:///modules/ytlaces/rc.d',
    source_permissions => 'use',
    owner              => $username,
  }


   file {"/home/$username/.rc.d/common":
    ensure => 'file',
    source => "puppet:///modules/ytlaces/rc.d/common",
    owner => $username,
   }
   
   file {"/home/$username/.rc.d/profile":
    ensure => 'file',
    source => "puppet:///modules/ytlaces/rc.d/common",
    owner => $username,
   }


   file {"/home/$username/.tmux.conf":
    ensure => 'file',
    source => "puppet:///modules/ytlaces/home/.tmux.conf",
    owner => $username,
   }
}
