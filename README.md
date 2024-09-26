# star-tracker

Astrophotography motorized tripod that 
tracks objects on the sky as earth rotates.
DIY el-cheapo.

![Tripod](/pic/tripod.jpg)

3D printable parts fit 3 small step motors
with M6 threaded rods as linear actuators for
each of 3 legs of a cheap camera tripod
"Vanguard VT-528A".

Motors are controled by a 3D printer motherboard
"SKR 1.3" with Marlin firmware (g-code) powered
from USB lithium battery. When all 3 motors are
powered, motherboard draws about 2A, so 5V/10Ah
battery can last for about 5h.

Simple python code is used to stabilize the picture.
Code works without any knowledge of star/planet
positions, time, geolocation or hardware geometry
(tripod lengths and angles).

Usage:

Place tripod and set motor actuators to
a position from which each leg has enough
stroke to shorten or lengthen for tracking
objects.

Run "./cursors.py" code. Motors will be driven
to XYZ = 0,0,0 position which is assumed as
initial position.

Manually point telephoto lens to any object on the sky,
tighten it mechanically and apply maximum zoom.

Use keys Ins/Del, Home/End, Page UP/Down and SHIFT
to center object in view. Those keys change
length of each of 3 tripod legs.
Keys without SHIFT make length change in steps of 0.1 mm,
Keys with SHIFT do it in steps of 1 mm.

When object is in the center, press SPACE. Machine
starts "learning".

As earth rotates, object moves from the center.

Use Ins/Del etc. keys to bring object to the center.
When object is in the center again, press RETURN.

Machine will "learn" user's centering
and keep centering in the same direction.

If object still drifts slowly from the
center, bring it mantually to the center
and press RETURN again. Centering can
be repeated any number of times and it
should refine.

BACKSPACE cancels manual centering done
after the last RETURN. After BACKSPACE,
motors wind back to position in the
direction learned from last RETURN.

If long time has passed since last SPACE or
camera is pointed to another object, press SPACE
to start new learning and repeat manualy centering
and pressing RETURN.
