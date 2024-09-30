// mechanical protection
// for motor connector and improvised cable plug

module connector_hole()
{
  cube([10,18,6.5],center=true);
}

module connector_holder()
{
  cube([20,25,8],center=true);
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
    motor_wire_space();
    board_wire_space();
    screw_in();
    screw_thru();
    translate([0,0,-50*half])
      cube([50,50,100],center=true);
  }
}

translate([-15,0,0])
motor_wire_holder(half=-1);
rotate([0,180,0])
translate([-15,0,0])
motor_wire_holder(half=1);
