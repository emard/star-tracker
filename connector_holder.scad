// mechanical protection
// for motor connector and improvised cable plug

module connector_hole()
{
  cube([10,20,6.0],center=true);
}

module connector_holder()
{
  cube([20,27,8],center=true);
}

module motor_wire_space()
{
  translate([0,11,0])
  cube([6.5,10,1.6],center=true);
}

module board_wire_space()
{
  translate([0,-11,0])
  cube([5,10,1.0],center=true);
}

module screw_in()
{
  for(i = [-1,1])
    translate([14/2*i,0,-0.01])
      cylinder(d=1.8,h=3,$fn=12);
}

module screw_thru()
{
  for(i = [-1,1])
    translate([14/2*i,0,0.01])
      rotate([180,0,0])
        cylinder(d=3,h=10,$fn=12);
}

module motor_wire_holder(half=1)
{
  difference()
  {
    connector_holder();
    connector_hole();
    if(half == 0) // for flat surface
    {
      translate([0,0,3-0.8+0.01])
      motor_wire_space();
      translate([0,0,3-0.5+0.01])
      board_wire_space();
      translate([0,0,3.25])
      screw_thru();  
      translate([0,0,50+3-0.01])
        cube([50,50,100],center=true);
    }
    else // standalone
    {
      motor_wire_space();
      board_wire_space();
      screw_in();
      screw_thru();
      translate([0,0,-50*half])
        cube([50,50,100],center=true);
    }
  }
}

if(0)
translate([-15,0,0])
motor_wire_holder(half=-1);
rotate([0,180,0])
if(0)
translate([-15,0,0])
motor_wire_holder(half=1);
if(1)
  motor_wire_holder(half=0);
  