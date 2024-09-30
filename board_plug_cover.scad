// mechanical protection
// for improvised board plug

module inside_hole()
{
  cube([10,6,5.5],center=true);
}

module connector_holder()
{
  cube([16,16,7],center=true);
}

/*
module motor_wire_space()
{
  translate([0,11,0])
  cube([6.5,10,1.4],center=true);
}
*/

module solder_space()
{
  translate([0,7,0])
  cube([5*2.54,10,5.5],center=true);
}

module board_wire_space()
{
  translate([0,-6,0.5-0.01])
  cube([5,9,1.0],center=true);
}

module screw_in()
{
  for(i = [-1,1])
    translate([5*2.54/2*i,-5,-0.01])
      cylinder(d=1.8,h=3,$fn=12);
}

module screw_thru()
{
  for(i = [-1,1])
    translate([5*2.54/2*i,0,0.01])
      rotate([180,0,0])
        cylinder(d=3,h=10,$fn=12);
}

module motor_wire_holder(half=1)
{
  difference()
  {
    connector_holder();
    inside_hole();
    solder_space();
    board_wire_space();
    screw_in();
    screw_thru();
    translate([0,0,-50*half])
      cube([50,50,100],center=true);
  }
}

motor_wire_holder(half=1);
