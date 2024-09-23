#!/usr/bin/env python3

# X (front) to east
# Y (right) to south west
# Z (left)  to north west

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

st_manual = np.array([ 0.0, 0.0, 0.0, 0.0])
st_target = np.array([ 0.0, 0.0, 0.0, 0.0])
st_speed  = np.array([ 2.0,-1.5, 0.5, 0.0])

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
  st_next[3] = sqrt(st_speed[0]*st_speed[0]+st_speed[1]*st_speed[1]+st_speed[2]*st_speed[2])
  # print("%8.2f %8.2f %8.2f %8.2f" % (st_next[0],st_next[1],st_next[2],st_next[3]))
  return st_next

def drain():
  for line in cnc.readline():
    continue

def position(x,y,z,feed):
  cnc.write(b"G1 X%.3f Y%.3f Z%.3f F%.3f\r" % (x,y,z,feed))
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

run = True
calc_every = 20
calc = 0
position(0,0,0,120)
waitcomplete()
while run:
    clock.tick(50) # FPS = frames per second this loop should run
    if calc == 0:
      st_target = calculate_future_position(1)
    automove = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            #keys = pygame.key.get_pressed()
            #rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * vel
            #rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * vel

            keyname = pygame.key.name(event.key)
            # print(pygame.key.name(event.key))
            if keyname == "insert":
              st_manual[0] += 1
            if keyname == "delete":
              st_manual[0] -= 1
            if keyname == "home":
              st_manual[1] += 1
            if keyname == "end":
              st_manual[1] -= 1
            if keyname == "page up":
              st_manual[2] += 1
            if keyname == "page down":
              st_manual[2] -= 1

            if keyname == "q":
              st_speed[0] += 0.1
            if keyname == "a":
              st_speed[0] -= 0.1
            if keyname == "w":
              st_speed[1] += 0.1
            if keyname == "s":
              st_speed[1] -= 0.1
            if keyname == "e":
              st_speed[2] += 0.1
            if keyname == "d":
              st_speed[2] -= 0.1
            # print(st_speed)

            st_final = st_target + st_manual
            x = st_final[0]
            y = st_final[1]
            z = st_final[2]
            position(x,y,z,120)

            waitcomplete()
            automove = False

    if automove:
      st_final = st_target + st_manual

      x = st_final[0]
      y = st_final[1]
      z = st_final[2]
      f = st_final[3]

      if calc == 0:
        position(x,y,z,f*1.1)
        print("XYZ = %8.2f%+.1f %8.2f%+.1f %8.2f%+.1f %8.2f" % (x,st_speed[0],y,st_speed[1],z,st_speed[2],f))
        waitcomplete()

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
