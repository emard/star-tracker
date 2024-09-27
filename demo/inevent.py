#!/usr/bin/env python3

# apt install python3-evdev

# https://python-evdev.readthedocs.io/en/latest/tutorial.html

from evdev import InputDevice, list_devices, ecodes, categorize
from select import select
from time import time

device_paths = ()
devices = [InputDevice(path) for path in list_devices()]
for device in devices:
    print(device.path, device.name, device.phys)
    if ecodes.EV_ABS in device.capabilities():
      # if "Joystick" in device.name:
        device_paths += (device.path,)

# A mapping of file descriptors (integers) to InputDevice instances.

#devices = map(InputDevice, ('/dev/input/event5', '/dev/input/event6'))
devices = map(InputDevice, device_paths)
devices = {dev.fd: dev for dev in devices}

for dev in devices.values(): print(dev)
# device /dev/input/event1, name "Dell Dell USB Keyboard", phys "usb-0000:00:12.1-2/input0"
# device /dev/input/event2, name "Logitech USB Laser Mouse", phys "usb-0000:00:12.0-2/input0"

select_timeout = 0.5 # [s] if no events return every 0.5 seconds
tnext = time() # next timer event
while True:
  r, w, x = select(devices, [], [], select_timeout)
  for fd in r:
    for event in devices[fd].read():
      # key pressed/released
      if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        strtype = ecodes.bytype[keyevent.event.type][keyevent.event.code]
        print(strtype)
      # analog paddle, ignore values near idle position 128 (120-136)
      if event.type == ecodes.EV_ABS and (event.value < 120 or event.value > 136):
        absevent = categorize(event) 
        strtype = ecodes.bytype[absevent.event.type][absevent.event.code]
        # print(strtype)
        if strtype == 'ABS_X':
          print("X", event.value)
        if strtype == 'ABS_Y':
          print("Y", event.value)
        if strtype == 'ABS_RX':
          print("RX", event.value)
        if strtype == 'ABS_RZ':
          print("RZ", event.value)
        if strtype == 'ABS_HAT0X':
          print("HATX", event.value)
        if strtype == 'ABS_HAT0Y':
          print("HATY", event.value)

  t = time()
  if t > tnext:
    tnext += 1 # timer every second
    print("t")

# event at 1351116708.002230, code 01, type 02, val 01
# event at 1351116708.002234, code 00, type 00, val 00
# event at 1351116708.782231, code 04, type 04, val 458782
