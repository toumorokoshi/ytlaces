# ytlaces

## Installing

1. clone this repo
1. install puppet
1. symlink repo to one of the following until it works:
  * `/etc/puppet/code/modules/` (possibly since puppet 4?)
  * `/opt/puppetlabs/puppet/modules/ytlaces`
  * `/etc/puppet/code/environments/standalone_puppet/modules`
4. install the following modules:
  *  `puppet module install puppetlabs-vcsrepo`
  *  `puppet module install puppetlabs-apt`
  *  `puppet module install puppet-archive`
4. Run the appropriate `bin/install_{env}`.
* `$ puppet apply examples/init.pp`

## installation into rc and profile

The following files serve the following purposes:

| filename          | purpose                                                                      |
| ----------------- | ---------------------------------------------------------------------------- |
| `$HOME/.xprofile` | yt-laces managed, for configuration that applies to all yt machines.         |
| `$HOME/.profile`  | user-managed, for configuration specific to the host.                        |
| `$HOME/.bashrc`   | user-managed, for configuration specific to the host. should source ytlaces. |

* add a section into your bash/zsh rc file that sources in a whole directory of rc files:

  `. $HOME/.ytlaces/init`

## post-install setup.

There's a couple more steps that need to run, post-install for now:


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
  - `ip link dev eno1 up`
  - `systemctl enable dhcpcd`
  - `systemctl start dhcpcd`

wifi-menu can be used to connect to the network.

Then run:

- `bin/install_yay`
- `yay -S install insync`

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