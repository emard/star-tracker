#!/usr/bin/env python3

# apt install python3-serial python3-numpy python3-evdev

# https://python-evdev.readthedocs.io/en/latest/tutorial.html

from evdev import InputDevice, list_devices, ecodes, categorize
from select import select
from time import time
from serial import Serial
from os import system
import numpy as np

# joystick button have embossed labels
# joystick button name = os name
ABS_LX      = "ABS_X"
ABS_LY      = "ABS_Y"
ABS_RY      = "ABS_RZ"
BTN_LT      = "BTN_BASE"   # mark object (start learning)
BTN_RT      = "BTN_BASE2"  # track object (from learning)
BTN_GREEN_A = "BTN_THUMB2" # faster (like SHIFT)
BTN_RED_B   = "BTN_THUMB"  # cancel manual
BTN_BACK    = "BTN_BASE3"  # all axis back to 0
BTN_START   = "BTN_BASE4"  # set this position as new 0
BTN_LB      = "BTN_TOP2"   # shutdown RPI together LB & RB
BTN_RB      = "BTN_PINKIE" # shutdown RPI together LB & RB

# ABS_RX      = "ABS_RX" # not used

# calculate next positions for auto and manual
def delta_position():
  global tp, st_track, st_manual
  tn = time()
  # tf is time in the future
  tf = tn  # [s] unix time float seconds since 1970
  tdelta = tf-tp
  tp = tf
  # delta position
  st_track  += st_speed_track  * tdelta/60
  st_manual += st_speed_manual * tdelta/60

def speed_limit():
  global st_speed_track, st_speed_manual
  for i in range(3):
    if st_speed_track[i] > max_speed:
      st_speed_track[i] = max_speed;
      print("limit track max")
    if st_speed_track[i] < -max_speed:
      st_speed_track[i] = -max_speed;
      print("limit track min")
    if st_speed_manual[i] > max_speed:
      st_speed_manual[i] = max_speed;
      print("limit manual max")
    if st_speed_manual[i] < -max_speed:
      st_speed_manual[i] = -max_speed;
      print("limit manual min")

# CNC functions

def drain():
  #return
  for line in cnc.readline():
    continue

def waitcomplete():
  #return
  cnc.write(b"M400\r")
  for line in cnc.readline():
    if line > 0 and line < 20: # probably "ok" response
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

st_speed_track  = np.array([ 0.0, 0.0, 0.0 ])
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
t  = t0

# max speed for each actuator
max_speed = 90 # [mm/min]
# max feed_rate for 3 actuators
max_feed_rate = 2*max_speed

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
#cnc = Serial(port='/dev/ttyS0', timeout=1)

waitcomplete()
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

run = True
feed_faster = 0.0 # [mm/min] to finish early, feed faster
feed_factor = 1.0 # adjusts hardware feed to real time
step_time = 0.2 # [s] control recalculation time
position(0,0,0,max_feed_rate) # reset initial position
waitcomplete()
fast = 1
notify = "" # small printed message about btn control

# main loop reads joystick and periodically runs timed loop

select_timeout = 0.1 # [s] if no events return every 0.1 seconds
tnext = t0 # next timer event
# joystick ideal idle value should be 127 or 128
# but actually it fluctuates around 124-132
# so readings within this range should be ignored
flat_lo = 124
flat_hi = 132
left_bumper = 0
right_bumper = 0

t_memory = t
st_memory = st_target.copy()
while True:
  r, w, x = select(devices, [], [], select_timeout)
  for fd in r:
    for event in devices[fd].read():
      # key pressed/released
      if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        strtype = ecodes.bytype[keyevent.event.type][keyevent.event.code]
        #print(strtype)
        if strtype == BTN_LT and event.value > 0: # left trigger
          # start learning
          t_memory = t
          st_memory = st_target.copy()
          notify += "*"
        if strtype == BTN_RT and event.value > 0: # right trigger
          # apply learned tracking
          st_speed_track = (st_target - st_memory) / (t - t_memory) * 60
          st_track = st_target.copy()
          st_manual *= 0
          notify += ">"
        if strtype == BTN_BACK: # small btn left of big silver btn
          # return to zero position and stop
          st_manual *= 0
          st_track  *= 0
          st_speed_track *= 0
          st_target *= 0
          t_memory = t
          st_memory = st_target.copy()
          notify += "E"
        if strtype == BTN_START: # small btn right of big silver btn
          # set current position as new origin and stop
          setorigin(0,0,0)
          st_manual *= 0
          st_track  *= 0
          st_speed_track  *= 0
          st_target *= 0
          t_memory = t
          st_memory = st_target.copy()
          notify += "0"
        if strtype == BTN_RED_B: # red button "B" cancel manual move, return to tracking
          st_manual *= 0
          notify += "/"
        if strtype == BTN_GREEN_A: # green button "A", faster move (like shift)
          if event.value:
            fast = 10
          else:
            fast = 1
        if strtype == BTN_LB: # left bumper
          left_bumper = event.value
        if strtype == BTN_RB: # right bumper
          right_bumper = event.value
        if left_bumper > 0 and right_bumper > 0: # both left+right bumper = shutdown
          system("sudo poweroff")
      # analog paddles readings changed
      if event.type == ecodes.EV_ABS: # and (event.value < flat_lo or event.value > flat_hi):
        absevent = categorize(event) 
        strtype = ecodes.bytype[absevent.event.type][absevent.event.code]
        # print(strtype)
        axis = -1
        if strtype == ABS_LX: # left X
          axis = 0
          direction = 1
        if strtype == ABS_LY: # left Y
          axis = 1
          direction = -1
        if strtype == ABS_RY: # right Y
          axis = 2
          direction = -1
        # RX axis not used
        #if strtype == ABS_RX:
        #  print("RX", event.value)
        #if strtype == 'ABS_HAT0X':
        #  print("HATX", event.value)
        #if strtype == 'ABS_HAT0Y':
        #  print("HATY", event.value)
        if axis >= 0:
          st_speed_manual[axis] = 0
          if event.value <= flat_lo:
            st_speed_manual[axis] = np.exp(0.1 * abs(event.value - flat_lo)) * (event.value - flat_lo) * direction * fast * 2.5E-7;
          if event.value >= flat_hi:
            st_speed_manual[axis] = np.exp(0.1 * abs(event.value - flat_hi)) * (event.value - flat_hi) * direction * fast * 2.5E-7;

  # periodic timer
  t = time()
  if t > tnext:
    late = 0
    if t - tnext > 2*step_time: # we came too late, reschedule
      tnext = t + 1
      waitcomplete()
      late = 1
      print("late")
    tnext += step_time # next timer event every second
    speed_limit()
    delta_position()
    st_target = st_track + st_manual
    t_target = time()
    st_delta = st_target - st_before
    t_delta = t_target - t_before
    feed_rate = np.linalg.norm(st_delta) / t_delta * 60
    feed_rate = feed_rate*feed_factor+feed_faster+(1+10*late)
    if feed_rate > max_feed_rate:
      feed_rate = max_feed_rate
    x = st_target[0]
    y = st_target[1]
    z = st_target[2]
    position(x,y,z,feed_rate)
    report = "%+8.2f%+.1f%+8.2f%+.1f%+8.2f%+.1f %s" % (x,st_speed_track[0],y,st_speed_track[1],z,st_speed_track[2],notify)
    notify = ""
    print(report)
    st_before = st_target.copy()
    t_before = t_target
