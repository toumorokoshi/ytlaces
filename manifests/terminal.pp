 class ytlaces::terminal{
   package {"termite":}

   file {"/home/tsutsumi/.config/termite":
    ensure => 'directory',
    owner => "tsutsumi"
   }

   file {"/home/tsutsumi/.config/termite/config":
    ensure => 'file',
    source => "puppet:///modules/ytlaces/.config/termite/config",
    owner => "tsutsumi"
   }
}
