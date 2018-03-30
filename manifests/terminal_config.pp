 class ytlaces::terminal_config{
   file {"/home/tsutsumi/.rc.d/":
    ensure => 'directory',
    owner => "tsutsumi"
   }

   file {"/home/tsutsumi/.rc.d/common":
    ensure => 'file',
    source => "puppet:///modules/ytlaces/rc.d/common",
    owner => "tsutsumi"
   }
}
