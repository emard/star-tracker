include <clamp3pod.scad>
include <motor_holder.scad>
include <linactuator.scad>
/*---------------
size = 1.0; // small
// size = 1.2; // middle
for(i=[-1,1])
  translate([0,-i])
     print_clamp_half(i,size);
*/

actuator_pos = [-26,-30,  0];
actuator_rot = [  0,  0, 45];

module actuator_holder()
{
  difference()
  {
    translate([5,0,2])
    cube([35,25,4],center=true);
    cylinder(d=7,h=10,$fn=16,center=true);
    for(i=[-1,1])
      for(j=[-1,1])
        translate([i*15/2,j*15/2])
          cylinder(d=2,h=40,$fn=16,center=true);
  }
}

module actuator_holder_3pod()
{
  scal=1.2;
  // [[xyz pos], height],
  clamps =
  [
    [[0,0, 37  ],12],
    [[0,0, 21.5],19],
    [[0,0, 6   ],12],
  ];
  clamp_trans = [0,0,9];
  clamp1_rot = [180,0,0];
  difference()
  {
    union()
    {
    for(ct = clamps)
    translate(ct[0])
      rotate(clamp1_rot)
        {
          print_clamp_half(i=-1,size=scal,height=ct[1]);
        }
    translate(actuator_pos)
      rotate(actuator_rot)
        translate([0,0,14.15])
        rotate([180,0,0])
        linactuator();
        //actuator_holder();
      // holder reinforcement
      if(1)
      translate([-8,-12,12])
        rotate(actuator_rot)
        translate([-5.5,0,0])
        cube([20,25,24],center=true);
    }
    if(1)
    for(ct = clamps)
    translate(ct[0])
      rotate(clamp1_rot)
      rotate(clamp_rot)
      scale([scal,scal,1])
      translate(rod_pos)
          rod_profile(h=100,s=1);
  }
    
}

module actuator_clamp()
{
   scal=1.2;
   clamp1_rot = [180,0,0];
   rotate(clamp1_rot)
     print_clamp_half(i=1,size=scal,height=10);
}

//actuator_holder_3pod();
actuator_clamp();
