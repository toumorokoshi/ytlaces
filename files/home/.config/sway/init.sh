#!/usr/bin/env bash
export XDG_CURRENT_DESKTOP=ubuntu:GNOME
export XDG_MENU_PREFIX=gnome
# start chrome next, so authcli doesn't fail.
google-chrome --profile-directory="Profile 1"
# finally start authcli
/usr/bin/authcli fastpass proxy -debug > /tmp/fastpass.log &
# maybe start ssh