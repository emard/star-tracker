#!/usr/bin/env python3

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import *
import intersect3sphere

# approx solve tripod as intersect of 3 spheres
# neglect size of small top triangle

# points where tripod touches the floor
px = [ 0.50,  0.00,  0.00 ]
py = [-0.30,  0.50,  0.00 ]
pz = [-0.30, -0.50,  0.00 ]
# lengths of tripod legs
lx = 0.8
ly = 0.8
lz = 0.8

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for n in range(20):
  lx = 0.7 + n*0.01
  # imagine each tripod leg as radius of the sphere
  # find 2 points in space where such 3 spehers intersect
  intersect = intersect3sphere.trilaterate(
  np.array(px), np.array(py), np.array(pz), lx, ly, lz)
  #print("sphere intersect", intersect)

  # approx camera mount points from middle point of
  # floor triangle to top of the tripod

  # assume that camera is on the point which is upper (largest z)
  if intersect[1][2] > intersect[0][2]:
    camera_position   = intersect[1]
  else:
    camera_position   = intersect[0]

  camera_heading_tail = (np.array(px)+np.array(py)+np.array(pz))/3
  # print("camera_heading_tail", camera_heading_tail)

  camera_heading = camera_position - camera_heading_tail
  camera_heading /= np.linalg.norm(camera_heading)

  #print("cam pos", camera_position, "cam head", camera_heading)

  # assemble vector array for plotting
  vectors = np.array([
  np.append(camera_position, px),
  np.append(camera_position, py),
  np.append(camera_position, pz),
  np.append(camera_position, camera_position+camera_heading/5)
  ])
  #print(vectors)

  # convert tail,head to tail,heading
  # which is the required input for arrow
  # plotting with "quiver" function
  for v in vectors:
    v[3:] -= v[:3]
  # vectors are changed in-place
  # print(vectors)

  X, Y, Z, U, V, W = zip(*vectors)
  ax.quiver(X, Y, Z, U, V, W)
  ax.set_xlim([-1.1, 1.1])
  ax.set_ylim([-1.1, 1.1])
  ax.set_zlim([-0.1, 1.1])
  plt.draw()
  plt.pause(1.0)
  ax.cla()
