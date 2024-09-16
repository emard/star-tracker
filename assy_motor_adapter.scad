include <motor.scad>
include <sprocket_adapter_0.8mm_nozzle.scad>
include <rod_holder.scad>
include <motor_holder.scad>

translate([0,-28,0])
{

translate([0,0,60])
rotate([180,0,0])
{
%motor();
translate([0,0,33.0])
rotate([180,0,0])
for(i=[0:1])
  rotate([0,0,180*i])
    sprocket_adapter();
translate([0,0,33])
  rod_holder();
//rod
translate([0,0,30])
%cylinder(d=3,h=130,$fn=12);
}

motor_holder();
}

%linear_extrude(height = 3, center = true, convexity = 1, $fn=64)
   import (file = "ploca-cnc.dxf", layer = "steel");
   