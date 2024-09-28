#!/usr/bin/env python3

# apt install python3-evdev

# https://python-evdev.readthedocs.io/en/latest/tutorial.html

from evdev import InputDevice, list_devices, ecodes, categorize
from select import select
from time import time
from serial import Serial
import numpy as np

# calculate next tracking position
def delta_position():
  global tp
  tn = time()
  # tf is time in the future
  tf = tn  # [s] unix time float seconds since 1970
  tdelta = tf-tp
  tp = tf
  # delta position
  return (st_speed + st_speed_manual) * tdelta/60

# CNC functions

def drain():
  #return
  for line in cnc.readline():
    continue

def waitcomplete():
  #return
  cnc.write(b"M400\r")
  for line in cnc.readline():
    if line < 20: # probably "ok" response
      break
  drain()

def setorigin(x,y,z):
  cnc.write(b"G92 X%.2f Y%.2f Z%.2f\r" % (x,y,z))
  drain()

def position(x,y,z,feed):
  cnc.write(b"G1 X%.2f Y%.2f Z%.2f F%.2f\r" % (x,y,z,feed))
  drain()

# global 3D vectors for star tracking

st_before = np.array([ 0.0, 0.0, 0.0 ])
st_target = np.array([ 0.0, 0.0, 0.0 ])
st_memory = np.array([ 0.0, 0.0, 0.0 ])
st_delta  = np.array([ 0.0, 0.0, 0.0 ])

st_speed  = np.array([ 0.0, 0.0, 0.0 ])
st_speed_manual = np.array([ 0.0, 0.0, 0.0 ])

st_track  = np.array([ 0.0, 0.0, 0.0 ]) # auto tracking
st_manual = np.array([ 0.0, 0.0, 0.0 ]) # manual change

# timing

t_target  = 0
t_before  = 0
t_memory  = 0

# time when program started

t0 = time()
tp = t0

# USB joystick

device_paths = ()
devices = [InputDevice(path) for path in list_devices()]
for device in devices:
    print(device.path, device.name, device.phys)
    if ecodes.EV_ABS in device.capabilities():
      # if "Joystick" in device.name:
        device_paths += (device.path,)

# A mapping of file descriptors (integers) to InputDevice instances.

# devices = map(InputDevice, ('/dev/input/event5', '/dev/input/event6'))
devices = map(InputDevice, device_paths)
devices = {dev.fd: dev for dev in devices}

for dev in devices.values(): print(dev)
# device /dev/input/event1, name "Dell Dell USB Keyboard", phys "usb-0000:00:12.1-2/input0"
# device /dev/input/event2, name "Logitech USB Laser Mouse", phys "usb-0000:00:12.0-2/input0"

# open and initialize CNC machine

cnc = Serial(port='/dev/ttyACM0', timeout=1)
#cnc = serial.Serial(port='/dev/ttyS0', timeout=1)

cnc.write(b"M92 X1600 Y1600 Z1600\r") # 1600 steps per mm
drain()
cnc.write(b"M92\r")
drain()

# set currents max 800mA enough for 5V
cnc.write(b"M906 X800 Y800 Z800\r")
drain()

cnc.write(b"G90\r") # absolute mode
drain()
cnc.write(b"M18 S5 X Y Z\r") # release motor power after 5s idle
drain()
# turn green LED on
#cnc.write(b"M106\r")
#drain()

# star tracking loop globals

responsive_countdown = 5
run = True
feed_more = 0.1 # [mm/min] to finish feed a bit early than control loop repeats
step_time = 1 # [s] control recalculation time
fps = 10 # [1/s] frames per second to read keys and draw
calc_every = step_time * fps
calc = 0 # counter
resync_every = 60 # every min one resync
resync = 0
notify = " " # to print what is memorized and set tracking
position(0,0,0,120) # reset initial position
waitcomplete()
fast = 1

# main loop reads joystick and periodically runs timed loop

select_timeout = 0.1 # [s] if no events return every 0.1 seconds
tnext = t0 # next timer event
# joystick values that fluctuate near idle position should be ignored
flat_lo = 120
flat_hi = 136
while True:
  r, w, x = select(devices, [], [], select_timeout)
  for fd in r:
    for event in devices[fd].read():
      # key pressed/released
      if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        strtype = ecodes.bytype[keyevent.event.type][keyevent.event.code]
        #print(strtype)
        if strtype == "BTN_BASE": # left trigger
          # start learning
          t_memory = t
          st_memory = st_target.copy()
          notify = "*"
        if strtype == "BTN_BASE2": # right trigger
          # apply learned tracking
          st_speed = (st_target - st_memory) / (t - t_memory) * 60
          st_track = st_target.copy()
          st_manual *= 0
          notify = ">"
        if strtype == "BTN_BASE3": # small btn left of big silver btn
          # return to zero position and stop
          st_manual *= 0
          st_track  *= 0
          st_speed  *= 0
          notify = "E"
        if strtype == "BTN_BASE4": # small btn right of big silver btn
          # set current position as new origin
          setorigin(0,0,0)
          st_manual *= 0
          st_track  *= 0
          st_speed  *= 0
          notify = "0"
        #if strtype == "BTN_THUMB": # red button "B"
        if strtype == "BTN_THUMB2": # green button "A"
          if event.value:
            fast = 10
          else:
            fast = 1
      # analog paddle, ignore values near idle position 128 (120-136)
      if event.type == ecodes.EV_ABS: # and (event.value < flat_lo or event.value > flat_hi):
        absevent = categorize(event) 
        strtype = ecodes.bytype[absevent.event.type][absevent.event.code]
        # print(strtype)
        axis = -1
        if strtype == 'ABS_X': # left X
          axis = 0
          direction = 1
        if strtype == 'ABS_Y': # left Y
          axis = 1
          direction = -1
        if strtype == 'ABS_RZ': # right Y
          axis = 2
          direction = -1
        # RX axis not used
        #if strtype == 'ABS_RX':
        #  print("RX", event.value)
        if strtype == 'ABS_HAT0X':
          print("HATX", event.value)
        if strtype == 'ABS_HAT0Y':
          print("HATY", event.value)
        if axis >= 0:
          st_speed_manual[axis] = 0
          if event.value < flat_lo:
            st_speed_manual[axis] = np.exp(1E-1 * abs(event.value - flat_lo)) * (event.value - flat_lo) * direction * fast * 1E-6;
          if event.value > flat_hi:
            st_speed_manual[axis] = np.exp(1E-1 * abs(event.value - flat_hi)) * (event.value - flat_lo) * direction * fast * 1E-6;
          responsive_countdown = 3

  # periodic timer
  t = time()
  if t > tnext:
    if t - tnext > 2*step_time: # we came too late, reschedule
      tnext = t
      waitcomplete()
    tnext += step_time # next timer event every second
    st_track += delta_position()
    st_target = st_track + st_manual
    t_target = time()
    st_delta = st_target - st_before
    t_delta = t_target - t_before
    feed_rate = np.linalg.norm(st_delta) * t_delta * 60 + 6 * responsive_countdown + 0.01
    if feed_rate > 60:
      feed_rate = 60
    if responsive_countdown:
      responsive_countdown -= 1
    x = st_target[0]
    y = st_target[1]
    z = st_target[2]
    position(x,y,z,feed_rate)
    report = "%+8.2f%+.1f%+8.2f%+.1f%+8.2f%+.1f %s" % (x,st_speed[0],y,st_speed[1],z,st_speed[2],notify)
    notify = " "
    print(report)
    st_before = st_target.copy()
    t_before = t_target
    #if resync < resync_every:
    #  resync += 1
    #else:
    #  resync = 0
    #  print("waiting for resync")
    #  waitcomplete()