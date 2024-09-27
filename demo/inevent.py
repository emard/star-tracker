#!/usr/bin/env python3

# apt install python3-evdev

# https://python-evdev.readthedocs.io/en/latest/tutorial.html

from evdev import InputDevice
from select import select

# A mapping of file descriptors (integers) to InputDevice instances.

devices = map(InputDevice, ('/dev/input/event0', '/dev/input/event5'))
devices = {dev.fd: dev for dev in devices}

for dev in devices.values(): print(dev)
# device /dev/input/event1, name "Dell Dell USB Keyboard", phys "usb-0000:00:12.1-2/input0"
# device /dev/input/event2, name "Logitech USB Laser Mouse", phys "usb-0000:00:12.0-2/input0"

while True:
   r, w, x = select(devices, [], [], 1)
   for fd in r:
       for event in devices[fd].read():
           print(event)
   print("t")

# event at 1351116708.002230, code 01, type 02, val 01
# event at 1351116708.002234, code 00, type 00, val 00
# event at 1351116708.782231, code 04, type 04, val 458782
