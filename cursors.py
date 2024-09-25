#!/usr/bin/env python3

# motor/leg position

# X (front) to east
# Y (right) to south west
# Z (left)  to north west

#  X
# Z Y

# manual position control

#                  Image move
# Insert     X++   down
# Delete     X--   up
# Home       Y++   up right
# End        Y--   down left
# Page Up    Z++   up left
# Page Down  Z--   down right

# manual speed control

#                  Image speed
# Q          Xs++  down
# A          Xs--  up
# W          Ys++  up right
# S          Ys--  down left
# E          Zs++  up left
# D          Zs--  down right

import pygame
import serial
import time
import numpy as np
from math import *

# time when program started
t0 = time.time()
tp = t0

# lets use x,y,z,f (4-vector) to describe spacetime state
# f is feed rate mm/min
# initial position motors at xyz=0, current time

st_manual = np.array([ 0.0, 0.0, 0.0 ])
st_target = np.array([ 0.0, 0.0, 0.0 ])
st_speed  = np.array([ 0.0, 0.0, 0.0 ])

# read current unix time (UTC)
# and calculate motor target position
# for short time dt [s] in the future
# to generate next g-code
# returns: (X,Y,Z,F)
# XYZ [mm]     position
# F   [mm/min] feed rate (currently not working)
def calculate_future_position(dt):
  global tp
  tn = time.time()
  # tf is time in the future
  tf = tn + dt # [s] unix time float seconds since 1970
  tdelta = tf-tp
  tp = tf
  # next position
  st_next = st_target + st_speed * tdelta/60
  # compute feed rate
  feed_rate = np.linalg.norm(st_speed)
  # print("%8.2f %8.2f %8.2f %8.2f" % (st_next[0],st_next[1],st_next[2],st_next[3]))
  return (st_next, feed_rate)

# simple functions

def drain():
  for line in cnc.readline():
    continue

def position(x,y,z,feed):
  cnc.write(b"G1 X%.2f Y%.2f Z%.2f F%.2f\r" % (x,y,z,feed))
  drain()

def waitcomplete():
  cnc.write(b"M400\r")
  for line in cnc.readline():
    if line < 20: # probably "ok" response
      break
  drain()

# main loop

cnc = serial.Serial(port='/dev/ttyACM0', timeout=1)

cnc.write(b"M92 X1600 Y1600 Z1600\r") # 1600 steps per mm
drain()
cnc.write(b"M92\r")
drain()
# turn green LED on
cnc.write(b"M106\r")
drain()
# set higher currents for 5V
if 0:
  cnc.write(b"M906 X1200 Y1200 Z1200\r")
  line = cnc.readline()
  print(line)
  cnc.write(b"M906\r")
  for i in range(5):
    cnc.readline()
    print(line)
  # set stealth mode off
  cnc.write(b"M569 S0 X Y Z\r")
  line = cnc.readline()
  print(line)
  cnc.write(b"M569\r")
  for i in range(5):
    cnc.readline()
    print(line)
cnc.write(b"G90\r") # absolute mode
drain()
cnc.write(b"M18 S5 X Y Z\r") # inactive release power 5 s
drain()
pygame.init()
window = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

rect = pygame.Rect(0, 0, 20, 20)
rect.center = window.get_rect().center
vel = 10

x=0
y=0
z=0
tvel = 1 # cnc motor velocity

responsive_countdown = 0
run = True
step_time = 1 # [s] control recalculation time
fps = 10 # [1/s] frames per second to read keys and draw
calc_every = step_time * fps
calc = 0 # counter
position(0,0,0,120) # reset initial position
waitcomplete()
while run:
    clock.tick(fps) # FPS = frames per second this loop should run
    if calc == 0:
      (st_target, feed_rate) = calculate_future_position(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            #keys = pygame.key.get_pressed()
            #rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * vel
            #rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * vel

            mods = pygame.key.get_mods()
            if mods & 3: # if left or right shift is pressed
              manualstep = 1 # large step
            else: # no shift
              manualstep = 0.1 # small step

            keyname = pygame.key.name(event.key)
            # print(pygame.key.name(event.key))
            if keyname == "insert":
              st_manual[0] += manualstep
            if keyname == "delete":
              st_manual[0] -= manualstep
            if keyname == "home":
              st_manual[1] += manualstep
            if keyname == "end":
              st_manual[1] -= manualstep
            if keyname == "page up":
              st_manual[2] += manualstep
            if keyname == "page down":
              st_manual[2] -= manualstep

            if keyname == "q":
              st_speed[0] += manualstep
            if keyname == "a":
              st_speed[0] -= manualstep
            if keyname == "w":
              st_speed[1] += manualstep
            if keyname == "s":
              st_speed[1] -= manualstep
            if keyname == "e":
              st_speed[2] += manualstep
            if keyname == "d":
              st_speed[2] -= manualstep
            # print(st_speed)
            responsive_countdown = 5

    if True:
      st_final = st_target + st_manual

      x = st_final[0]
      y = st_final[1]
      z = st_final[2]

      if calc == 0:
        if responsive_countdown:
          responsive_countdown -= 1
          position(x,y,z,30) # fast position
        else:
          position(x,y,z,feed_rate*1.1) # feed slightly faster to prevent buffer overflow
          waitcomplete()
        print("XYZ = %8.2f%+.1f %8.2f%+.1f %8.2f%+.1f" % (x,st_speed[0],y,st_speed[1],z,st_speed[2]))

    rect.centerx = st_final[0] * 100
    rect.centery = st_final[1] * 100

    # print("XYZ = %7.1f %7.1f %7.1f" % (x,y,z))

    rect.centerx = rect.centerx % window.get_width()
    rect.centery = rect.centery % window.get_height()

    window.fill(0)
    pygame.draw.rect(window, (255, 0, 0), rect)
    pygame.display.flip()

    if calc < calc_every:
      calc += 1
    else:
      calc = 0

pygame.quit()
exit()
