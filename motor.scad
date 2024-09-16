module motor()
{
  dscrw=31;
  dwide=39;
  lhigh=32.5;
  laxis=16.7;
  daxis=5;
  dround=8;
  dcircle=22;
  hcircle=1.8;
  hsprocket=4.3; // from motor screw front to d1 sprocket
  d1sprocket=13;
  l1sprocket=8.0;
  d2sprocket=16.8;
  l2sprocket=4;

  difference()
  {
  minkowski()
  {
    cube([dwide-dround,dwide-dround,lhigh/2],center=true);
    cylinder(d=dround,h=lhigh/2,center=true,$fn=32);
  }
    for(i=[0:3])
      rotate([0,0,i*90])
        translate([dscrw/2,dscrw/2,lhigh/2-4.9])
          cylinder(d=3,h=lhigh,$fn=16);
  }
  // circle with axis bearing
  translate([0,0,lhigh/2])
    cylinder(d=dcircle,h=hcircle,$fn=64);
  // the axis
  translate([0,0,lhigh/2])
    cylinder(d=daxis,h=laxis,$fn=64);
  // smaller diameter sprocket
  translate([0,0,lhigh/2+hsprocket])
    cylinder(d=d1sprocket,h=l1sprocket,$fn=20);
  // larger diameter sprocket
  translate([0,0,lhigh/2+hsprocket+l1sprocket])
    cylinder(d=d2sprocket,h=l2sprocket,$fn=40);
}

//motor();
