include <clamp3pod.scad>
include <motor_holder.scad>

// todo drill clamp screw holes deeper near reinforcement
// todo 3 holes for hall sensor
/*
size = 1.0; // small
// size = 1.2; // middle
for(i=[-1,1])
  translate([0,-i])
     print_clamp_half(i,size);
*/

motor_pos = [ -26, -30,  0];
motor_rot = [   0,  0,  45];

module motor_holder_3pod()
{
  // [[xyz pos], height],
  clamps = [
    [[0,0, -3],12],
    [[0,0,-18.5],19],
    [[0,0,-34],12],
    ];
  clamp1_rot = [180,0,0];
  difference()
  {
    union()
    {
    for(ct = clamps)
    translate(ct[0])
      rotate(clamp1_rot)
        {
              print_clamp_half(i=-1,size=1.0,height=ct[1]);
        }
    translate(motor_pos)
      rotate(motor_rot)
      {
        motor_holder();
        // holder box reinforcement
        motor_box();
      }        
    }
    if(1)
    for(ct = clamps)
    translate(ct[0])
      rotate(clamp1_rot)
      rotate(clamp_rot)
      translate(rod_pos)
          rod_profile(h=100,s=1);
  }
    
}

module motor_clamp()
{
  print_clamp_half(i=1,size=1.0);
}

//motor_holder_3pod();
motor_clamp();
