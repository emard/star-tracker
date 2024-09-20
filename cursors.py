#!/usr/bin/env python3

import pygame
import serial
import time
import numpy as np

# time when program started
t0 = time.time()

# lets use x,y,z,t (4-vector) to describe spacetime state
# initial position motors at xyz=0, current time

st_target = np.array([0,0,0,t0])
# st_last   = st_target.copy()

# read current unix time (UTC)
# and calculate motor target position
# for short time dt [s] in the future
# to generate next g-code
# returns: (X,Y,Z,F)
# XYZ [mm]   position
# F   [mm/s] feed rate
def calculate_future_position(dt):
  tn = time.time()
  # tf is time in the future
  tf = tn + dt # [s] unix time float seconds since 1970
  feed_rate = 2.2 # [mm/min]
  # next position
  st_next = np.array([(tf-t0)/60*2.2,0,0,tf])
  # print("%8.2f %8.2f %8.2f %15.2f" % (st_next[0],st_next[1],st_next[2],st_next[3]))
  st_target = st_next;
  return st_next

# main loop

cnc = serial.Serial(port='/dev/ttyACM0', timeout=1)

cnc.write(b"M92 X3200 Y3200 Z3200\r") # steps per mm
line = cnc.readline()
cnc.write(b"M92\r")
line = cnc.readline()
print(line)
# turn green LED on
cnc.write(b"M106\r")
line = cnc.readline()
print(line)
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
line = cnc.readline()
print(line)
cnc.write(b"M18 S1 X Y Z\r") # inactive release power 1 s
line = cnc.readline()
print(line)

pygame.init()
window = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

rect = pygame.Rect(0, 0, 20, 20)
rect.center = window.get_rect().center
vel = 1

x=0
y=0
z=0
tvel = 1 # cnc motor velocity

run = True
while run:
    clock.tick(10) # FPS = frames per second this loop should run
    calculate_future_position(1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:

            keys = pygame.key.get_pressed()

            rect.x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * vel
            rect.y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * vel

            x += (keys[pygame.K_RIGHT]    - keys[pygame.K_LEFT]    ) * tvel
            y += (keys[pygame.K_UP]       - keys[pygame.K_DOWN]    ) * tvel
            z += (keys[pygame.K_PAGEUP]   - keys[pygame.K_PAGEDOWN]) * tvel
            cnc.write(b"G1 X%.0f Y%.0f Z%.0f F30\r" % (x,y,z))
            line = cnc.readline()
            print(pygame.key.name(event.key),line)
            print("XYZ = %5.0f %5.0f %5.0f" % (x,y,z))

            rect.centerx = rect.centerx % window.get_width()
            rect.centery = rect.centery % window.get_height()

            window.fill(0)
            pygame.draw.rect(window, (255, 0, 0), rect)
            pygame.display.flip()

pygame.quit()
exit()
