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

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    # unit vectors
    v1_u = v1 / np.linalg.norm(v1)
    v2_u = v2 / np.linalg.norm(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

# main code

animate = False

if animate:
  plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for n in range(1):
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

  # simple camera heading
  # make 2 unit vectors along 2 tripod legs
  # camera heading is a vector defined by 2 heads of unit vector
  # here we make all 3 unit vectors for code symmetry but only 2 needed
  px1  = px-camera_position;
  px1 /= np.linalg.norm(px1)
  py1  = py-camera_position;
  py1 /= np.linalg.norm(py1)
  pz1  = pz-camera_position;
  pz1 /= np.linalg.norm(pz1)

  camera_heading = py1-pz1;
  camera_heading /= np.linalg.norm(camera_heading)

  # fake camera just top vector
  # camera_heading = np.array([0,0,1])

  # simple floor heading
  # make 2 unit vectors along 2 tripod legs
  # floor heading is a vector defined by legs of tripod
  fx = np.array(px)-np.array(pz)
  floor_x = fx / np.linalg.norm(fx) # unit vector for tripod heading

  fy = np.array(py)-np.array(pz)
  floor_z = np.cross(fx,fy)
  floor_z /= np.linalg.norm(floor_z) # unit vector for tripod heading

  floor_y =  np.cross(floor_x,floor_z)
  floor_y /= np.linalg.norm(floor_y) # unit vector for tripod heading

  print("unit %.2f %.2f %.2f" % (np.linalg.norm(floor_x),np.linalg.norm(floor_y),np.linalg.norm(floor_z),))

  # use dot product to calculate projection of camera heading
  # to floor xyz coordinate system
  # camera angle (related to floor coordinate system)
  # can be calculated as angles of this vector
  cam2floor = np.array([
    np.dot(camera_heading,floor_x),
    np.dot(camera_heading,floor_y),
    np.dot(camera_heading,floor_z)])
  # azimouth and elevation
  a = np.degrees(np.arctan(cam2floor[0]/cam2floor[1]))
  e = np.degrees(np.arctan(cam2floor[2]/cam2floor[1]))

  # assemble vector array for plotting
  vectors = np.array([
  np.append(camera_position, px),
  np.append(camera_position, py),
  np.append(camera_position, pz),
  np.append(camera_position, camera_position+camera_heading/5), # camera heading
  np.append(px, px+floor_x/5), # floor heading x
  np.append(px, px+floor_y/5), # floor normal y
  np.append(px, px+floor_z/5), # floor normal z
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
  # angle
  print("cam       XYZ = %.2f %.2f %.2f" % (camera_heading[0],camera_heading[1],camera_heading[2],))
  print("floor_x   XYZ = %.2f %.2f %.2f" % (floor_x[0],floor_x[1],floor_x[2],))
  print("floor_y   XYZ = %.2f %.2f %.2f" % (floor_y[0],floor_y[1],floor_y[2],))
  print("floor_z   XYZ = %.2f %.2f %.2f" % (floor_z[0],floor_z[1],floor_z[2],))
  print("cam2floor XYZ = %.2f %.2f %.2f" % (cam2floor[0],cam2floor[1],cam2floor[2],))
  print("azimuth=%.2f° elevation=%.2f°"  % (a,e))
  # print("angle %.2f° (should return 90°)" % (angle_between(np.array([1,0,0]),np.array([0,1,0])) * 180/pi ))
  if animate:
    plt.pause(1.0)
    ax.cla()

if not animate:
  plt.show()
