module nut_cutter(w=5.65,depth=6,ins_delta=0.4,ins_depth=2,trans_depth=3)
{
    d=0; // z position
    chep_nut_d=w * (2/sqrt(3)); // nut tight hex
    chep_nut_depth=depth; // total depth
    chep_nut_ins_d=chep_nut_d+ins_delta; // enlarged insertion hex
    chep_nut_ins_depth=ins_depth; // insertion depth
    chep_nut_transition_depth=trans_depth; // easier 3D print, conical transition

    // duboki tijesni utor za maticu
    translate([0,0,-d/2+chep_nut_depth/2-0.001])
      cylinder(d=chep_nut_d,h=chep_nut_depth,$fn=6,center=true);
    // plitki labavi utor za maticu
    translate([0,0,-d/2+chep_nut_ins_depth/2-0.001])
      cylinder(d=chep_nut_ins_d,h=chep_nut_ins_depth,$fn=6,center=true);
    // konusni prijelaz za lakše printanje
    if(1)
    translate([0,0,-d/2+chep_nut_depth+chep_nut_transition_depth/2-0.001])
      cylinder(d1=chep_nut_d,d2=0,h=chep_nut_transition_depth+0.005,$fn=6,center=true);
}

module head_cutter(d=6,h=5)
{
  delta=0.01;
  translate([0,0,-delta])
  cylinder(d=d,h=h+2*delta,$fn=32);
  translate([0,0,h])
    cylinder(d1=d,d2=0,h*2/3,$fn=32);
    
}

//nut_cutter();
//head_cutter();

