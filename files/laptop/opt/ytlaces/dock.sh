#!/bin/sh
set -e

dock () {
    # collect the thunderbolt device name
    device_name=`cat /sys/bus/thunderbolt/devices/0-1/device_name`
    if [ -f "/tmp/is_docked" ]; then
        currently_docked_device=`cat /tmp/is_docked`
    fi
    x_owner=`ps auxf | grep "xrandr" | cut -f 1 -d ' '`
    if [ "$device_name" == "TBT3-UDV Docking Station" ]; then
        su $x_owner /bin/sh -c "xrandr --display :0 --output eDP-1 --auto --output DP-1 --auto --right-of eDP-1"
    elif [ "$device_name" == "Core X Chroma" && "$currently_docked_device" != "Core X Chroma" ]; then
        cp /etc/X11/xorg.conf.egpu /etc/X11/xorg.conf
        rm /home/tsutsumi/.Xresources.d/laptop
        systemctl restart lightdm
    fi
    echo "$device_name" > /tmp/is_docked
}

undock () {
    device_name=`cat /tmp/is_docked`
    x_owner=`ps auxf | grep "xrandr" | cut -f 1 -d ' '`
    su $x_owner /bin/sh -c "xrandr --display :0 --output eDP-1 --auto --output DP-1 --off"
    if [ "$device_name" == "Core X Chroma" ]; then
        # we have to restart X, since we restarted it with the eGPU
        if [ -f "/etc/X11/xorg.conf" ]; then
            rm /etc/X11/xorg.conf
            systemctl restart lightdm
        fi
    fi
    cp /home/$x_owner/.Xresources.d/laptop.bak /home/$x_owner/.Xresources.d/laptop
    echo "undocked" > /tmp/is_docked
}

main () {
    op="$1"
    if [ "$op" = "dock" ]; then
        dock
    elif [ "$op" = "undock" ]; then
        undock
    fi
}

main $1