

module motor_base_plate(a=55,b=55,thick=3,d=10)
{
  minkowski()
  {
    difference()
    {
      cube([a-d,b-d,thick/2],center=true);
      // reduce unused material
      if(0)
      for(i=[-1:2:1])
      translate([50*i,-48,0])
        rotate([0,0,45*i])
          cube([100,100,thick/2+0.001],center=true);
    }
    // round edges
    cylinder(d=d,h=thick/2,$fn=32,center=true);
  }
}

module motor_spacer()
{
  spacer_len=21;
  d1=4.5; // inner dia
  d2=10;   // outer dia
  difference()
  {
    cylinder(d=d2,h=spacer_len,$fn=32);
    translate([0,0,-0.001])
      cylinder(d=d1,h=spacer_len+0.002,$fn=32);
  }
}

module motor_box()
{
screw_len = 9.5;
thick=3; // thickness of the holder
translate([0,0,screw_len-8-21.5])
  difference()
  {
    motor_base_plate(thick=40);
    // inside cut
    translate([0,0,-0.01])
    motor_base_plate(a=45,b=45,thick=41,d=7);
    // angular cut, print faster
    translate([-10-45/2,0,0])
      rotate([0,-45,0])
      cube([40,60,100],center=true);
  }
}

module motor_holder()
{
// coordinates for mounting screws
mountscrew_pos = [[-34,5,0],[0,-32,0],[34,5,0]];
motor_center = [0,0,0];
screw_len = 9.5;
thick=3; // thickness of the holder
d_mixer_hole=34; // should be ok for parts to go freely

// mount screws
if(0)
%for(i=[0:2])
  translate(mountscrew_pos[i])
    cylinder(d=4,h=screw_len,$fn=12);

translate([0,0,screw_len-8])
  difference()
  {
    motor_base_plate();
    // axis hole
    translate(motor_center)
      rotate([0,0,360/16])
      cylinder(d=d_mixer_hole,h=thick+0.001,$fn=8,center=true);
    // motor mounting 4 holes M3-thru
    translate(motor_center)
      for(i=[0:3])
        rotate([0,0,90*i])
          translate([-31.5/2,-31.5/2,0]) // motor holes positions
            cylinder(d=3.3,h=thick+0.001,$fn=12,center=true);
    // plate mounting 3 holes M4-thru
    if(0)
    for(i=[0:2])
      translate(motor_center+mountscrew_pos[i])
        cylinder(d=4.5,h=thick+0.001,$fn=12,center=true);

  }
}


if(0)
  motor_holder();

if(0)
  motor_spacer();
