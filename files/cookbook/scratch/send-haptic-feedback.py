#!/usr/bin/env python
# TODO: unfinished, I used `fftest` instead.
import pprint
from evdev import ecodes, InputDevice, list_devices, ff

devices = [InputDevice(path) for path in list_devices()]
stadia_device = None
for device in devices:
    if "Stadia" in device.name:
        stadia_device = device
print(stadia_device)
print(f"effect: {ecodes.EV_FF}")
print(ecodes.EV_FF in stadia_device.capabilities())
pprint.pprint(stadia_device.capabilities())

rumble = ff.Rumble(strong_magnitude=0x0000, weak_magnitude=0xFFFF)
effect_type = ff.EffectType(ff_rumble_effect=rumble)
duration_ms = 1000

effect = ff.Effect(
    ecodes.FF_RUMBLE, -1, 0, ff.Trigger(0, 0), ff.Replay(duration_ms, 0), effect_type
)

repeat_count = 1
effect_id = stadia_device.upload_effect(effect)
stadia_device.write(ecodes.EV_FF, effect_id, repeat_count)
stadia_device.erase_effect(effect_id)
