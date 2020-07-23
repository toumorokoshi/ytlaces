#!/bin/sh
set -e 

dock () {
    # collect the thunderbolt device name
    device_name=`cat /sys/bus/thunderbolt/devices/0-1/device_name`
    if [ "$device_name" == "TBT3-UDV Docking Station" ]; then
        xrandr --display :0 --output eDP-1 --auto --output DP-1 --auto --right-of eDP-1
    fi
    echo "$device_name" > /tmp/is_docked
}

undock () {
    echo "undocked" > /tmp/is_docked
    xrandr --display :0 --output eDP-1 --auto --output DP-1 --off
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