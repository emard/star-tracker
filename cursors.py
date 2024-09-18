#!/usr/bin/env python3

import pygame
import serial

cnc = serial.Serial('/dev/ttyACM0')

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
    clock.tick(60)
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
