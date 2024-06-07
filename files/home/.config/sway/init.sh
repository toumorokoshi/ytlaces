#!/usr/bin/env bash
export XDG_CURRENT_DESKTOP=ubuntu:GNOME
export XDG_MENU_PREFIX=gnome

# workaround to enable screenshare sway

# Import the WAYLAND_DISPLAY env var from sway into the systemd user session.
dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP=sway

# Stop any services that are running, so that they receive the new env var when they restart.
systemctl --user stop pipewire pipewire-media-session xdg-desktop-portal xdg-desktop-portal-wlr
systemctl --user start pipewire-media-session

# start chrome next, so authcli doesn't fail.
google-chrome --profile-directory="Profile 1"
# finally start authcli
/usr/bin/authcli fastpass proxy -debug > /tmp/fastpass.log &
# maybe start ssh