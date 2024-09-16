#!/usr/bin/env python3

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from math import *

vectors = np.array([
# tail      x,y,z,   head         x,y,z
[ 0.5,  0.0,  0.0,   0.05,  0   ,  1.00],
[-0.3,  0.5,  0.0,  -0.03,  0.05,  1.00],
[-0.3, -0.5,  0.0,  -0.03, -0.05,  1.00],
])

# convert tail,head to tail,heading
# which is the required input for arrow
# plotting with "quiver" function
for v in vectors:
  v[3:] -= v[:3]

#print(vectors)

X, Y, Z, U, V, W = zip(*vectors)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.quiver(X, Y, Z, U, V, W)
ax.set_xlim([-1.1, 1.1])
ax.set_ylim([-1.1, 1.1])
ax.set_zlim([-0.1, 1.1])
plt.show()
