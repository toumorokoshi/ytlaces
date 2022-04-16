# ytlaces

## Installing

* install puppet
* clone this repo
* symlink repo to one of:
  * `/opt/puppetlabs/puppet/modules/ytlaces`
  * `/etc/puppet/code/environments/standalone_puppet/modules`
* install the following modules:
  *  `puppet module install puppetlabs-vcsrepo`
  *  `puppet module install puppetlabs-apt`
  *  `puppet module install puppet-archive`

* `$ puppet apply examples/init.pp`

## post-install setup.

There's a couple more steps that need to run, post-install for now:

* add a section into your bash/zsh rc file that sources in a whole directory of rc files:

  `. $HOME/.ytlaces/init`

* add a resolv.conf line for google's 8.8.8.8 dns. This ensures that a public dns is used before a private one.
* ibus-setup

## Setting up from a fresh Windows install

* run disk manager ("Create and format hard disk partitions") in the search
* shrink main volume by desired amount.
* [disable UEFI secure boot (arch linux boot will not start without it)](https://wiki.archlinux.org/index.php/Dual_boot_with_Windows#UEFI_Secure_Boot)
* start arch linux boot partition
* follow setting up arch instructions

## Setting up Arch

* after installation, you may need to enable and start up network devices:
    ip link dev eno1 up
    systemctl enable dhcpcd
    systemctl start dhcpcd
* wifi-menu can be used to connect to the network.
    bin/install_yay
    yay -S install dropbox
    yay -S install dropbox-cli
    systemctl enable dropbox@tsutsumi

* dropbox
* dropbox-cli

## Testing

After installing ytlaces, the following should be validated:

* set password

## Troubleshooting

### CA certificates /etc/puppetlabs/puppet/ssl expired

- remove existing certs `sudo rm -r /etc/puppetlabs/ssl`
- install puppetserver (in arch AUR)
- run `sudo puppetserver ca setup`

## cannot find "::ytlaces"

for some reason I had to sudo as root, then do the apply to find the module. some new version of puppet has issues?

This seemed to be fixed by symlinking `ytlaces` into the `/usr/share/puppet/modules` directory, or by fixing the name of the class in `./metadata.json` to `ytlaces` instead of `yt-laces`.

I verified the puppet module was successfully installed with `puppet modules list` as root (since you need to root to run this file).

## notes / todos

- add bluetooth via blueman: https://github.com/blueman-project/blueman