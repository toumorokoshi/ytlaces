# Slice MK Keyboard

I use a SliceMK Ergodox Wireless LP keyboard on the go.

1. update the json file here
2. build a keymap using the [ZMK configurator on slicemk](https://config.slicemk.com/zmk/keymap/) using the custom config documented.
3. download the zip and extract it.
4. double-tap the right "reset" button on the keyboard or dongle to get it read for flashing.
5. connect it via usb-c
6. mount the new disk drive
7. copy the appropriate "zmk-left.uf2" file to the drive.
8. umount the disk drive (the flash will not occur until the unmounting occurs).

## Custom Config

Custom configuration should be put in the "Custom DeviceTree" section of the configurator, such as the following:

```
&mt {
    tapping-term-ms = <400>; // sometimes I hit special with the current config.
};
```

## Keyboard design decisions

- I originally mapped the 2u key on the left with space + hold for the super key. However this kept resulting in the super key getting triggered while I was typing because I tend to not left go of the space key in time (or the keyboard detects it as held). Either way I moved the mapping to the much-less-used end key (so super hold + end tap).