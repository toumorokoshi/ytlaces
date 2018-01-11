#!/usr/bin/env python
"""
This script can be run continuously, and will rotate the screen
according to the accelerometer
"""
from time import sleep
from os import path as op
import sys
from subprocess import check_call, check_output
from glob import glob

g = GRAVITY = 7.0  # (m^2 / s) sensibility, gravity trigger
DISABLE_TOUCHPADS = False
TOUCHSCREENS_NAMES = ['touchscreen', 'wacom', 'elan']
TOUCHPAD_NAMES = ['touchpad', 'trackpoint']

STATES = [
    {'rot': 'normal', 'coord': '1 0 0 0 1 0 0 0 1', 'touchpad': 'enable',
     'invert': '0', 'swap': '0', 'check': lambda x, y: y <= -g},
    {'rot': 'inverted', 'coord': '-1 0 1 0 -1 1 0 0 1', 'touchpad': 'disable',
     'invert': '1', 'swap': '0', 'check': lambda x, y: y >= g},
    {'rot': 'left', 'coord': '0 -1 1 1 0 0 0 0 1', 'touchpad': 'disable',
     'invert': '1', 'swap': '1', 'check': lambda x, y: x >= g},
    {'rot': 'right', 'coord': '0 1 0 -1 0 1 0 0 1', 'touchpad': 'disable',
     'invert': '0', 'swap': '1', 'check': lambda x, y: x <= -g},
]


def main():
    devices = check_output(['xinput', '--list', '--name-only']).decode().splitlines()

    touchscreens = _filter(devices, TOUCHSCREENS_NAMES)
    touchpads = _filter(devices, TOUCHPAD_NAMES)

    scale = float(read('in_accel_scale'))

    accel_x = bdopen('in_accel_x_raw')
    accel_y = bdopen('in_accel_y_raw')

    current_state = None

    while True:
        x = read_accel(accel_x, scale)
        y = read_accel(accel_y, scale)
        for i in range(4):
            if i == current_state:
                continue
            if STATES[i]['check'](x, y):
                current_state = i
                rotate(i, touchscreens, touchpads)
                break
        sleep(1)


def bdopen(fname):
    return open(op.join(basedir, fname))


def read(fname):
    return bdopen(fname).read()


def rotate(state, touchscreens, touchpads):
    s = STATES[state]
    check_call(['xrandr', '-o', s['rot']])
    for dev in touchscreens if DISABLE_TOUCHPADS else (touchscreens + touchpads):
        check_call([
            'xinput', 'set-prop', dev,
            'Coordinate Transformation Matrix',
        ] + s['coord'].split())
        # check_call([
        #  'xinput', 'set-prop', dev,
        #  'Evdev Axes Swap', s['swap']
        # ])
        # check_call([
        #  'xinput', 'set-prop', dev,
        #  'Evdev Axis Inversion',
        #  s['invert'], s['swap']
        # ])
        #check_call([
        #    'xinput', 'set-prop', dev,
        #    'Evdev Axes Inversion', '0'
        # + s['rot'].split())
        # xinput set-prop $input "Evdev Axis Calibration" ${cal[@]}
    if DISABLE_TOUCHPADS:
        for dev in touchpads:
            check_call(['xinput', s['touchpad'], dev])


def read_accel(fp, scale):
    fp.seek(0)
    return float(fp.read()) * scale

def _filter(value, input_list):
    return [i for i in value if any(
        j in i.lower() for j in input_list
    ) if "pen" not in i.lower()]

for basedir in glob('/sys/bus/iio/devices/iio:device*'):
    if 'accel' in read('name'):
        break
else:
    sys.stderr.write("Can't find an accellerator device!\n")
    sys.exit(1)

if __name__ == '__main__':
    main()
