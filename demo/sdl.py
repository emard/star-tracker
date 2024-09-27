#!/usr/bin/env python3

import os
import pygame
import time

def FindDisplayDriver():
  for driver in ["fbcon", "directfb", "svgalib"]:
    if not os.getenv("SDL_VIDEODRIVER"):
      os.putenv("SDL_VIDEODRIVER", driver)
    try:
      pygame.display.init()
      return True
    except pygame.error:
      pass
  return False

if __name__ == "__main__":
  pygame.init()
  if not FindDisplayDriver():
    print("Failed to initialise display driver")
  else:
    print("Filling screen red")
    pygame.mouse.set_visible(False)
    width  = pygame.display.Info().current_w
    height = pygame.display.Info().current_h
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    screen.fill((0xFF, 0, 0))
    pygame.display.update()
    time.sleep(5)
    pygame.quit()
