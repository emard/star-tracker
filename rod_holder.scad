include <nut_cutter.scad>

module rod_holder()
{
    drod=6.5; // rod hole dia
    xhole=22; // mount screw holes distance
    dhole=2.7; // mount screw hole dia
    dhead=5; // mount screw head dia
    hmount=3; // mount screw height from bottom
    box=[29,12,20]; // cube dimension
    hex_d=24; // hexagon reinforcement
    translate([0,0,box[2]/2])
    difference()
    {
      union()
      {
        cube(box,center=true);
        cylinder(d=hex_d,h=box[2],$fn=6,center=true);
      }
      // cut mounting screws
      for(i=[0:1])
        rotate([0,0,180*i])
          translate([xhole/2,0,0])
          {
            // screw bolt pass
            cylinder(d=dhole,h=box[2]+0.01,$fn=16,center=true);
            // screw head inlet
            translate([0,0,-box[2]/2+hmount])
              cylinder(d=dhead,h=box[2],$fn=16);
          }
      // cut rod
      cylinder(d=drod,h=box[2]+0.01,$fn=16,center=true);
      // cut nut holder
      translate([0,0,-box[2]/2])

      nut_cutter(w=10.5,depth=12,ins_delta=0.8,ins_depth=4,trans_depth=6);
    }
}

if(0)
  rod_holder();
