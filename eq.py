#!/usr/bin/env python3
from math import *

# 3nožac stoji na 3 točke
# 1 točka zapad spušta se nogar
# 2 točke istok fixne, čine "os" rotacije sjever
# korekcija 2 fixne točke nisu sasvim fixne
# jednu ipak treba malo micat tako da rotacija
# kamere bude u 3D osi sjevera

thread_pitch = 1.0 # mm thread pitch M6
r = 500 # mm tripod radius (from center to foot)
h3pod = 950 # mm tripod height
h = 135 # mm elevation per hour
steps = 200 # steps per turn

print("mm/min : %3.1f" % (h/60))
print("step/s : %3.1f" % (h/thread_pitch/3600*steps))
print(" deg/h : %3.1f" % (atan(h/r) * 180/pi))
print(" deg/h : %3.1f required" % (360/24))