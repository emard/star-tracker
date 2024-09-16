// clamp for tripod "Vanguard VT-528A"

clamp_rot = [0,0,-11];
rod_pos = [-6.5,-7,0];

module contour()
{
  polygon(points=[
    [  0.0,  0.0], // desno od polukruga
    [  6.3, -0.5], // unutarnja strana blago zakrivljeni dio, skoro ravni
    [ 13.5,  0.0], // tocka na sredini zakrivljenja
    [ 16.5,  5.0], // zakrivljeniji dio
    [ 16.5,  9.0], // tocka na srediji zakrivljenja
    [ 11.0, 15.0], // ravni kosi vanjski dio
    [ -1.0, 15.0], // ravni vanjski dio
    [ -4.0, 10.5], // tocka na sredini zakrivljenja
    [ -4.0,  5.0], // zakrivljeni dio
    [ -1.0,  4.0]  // tocka na sredini polukružnog dijela
  ]);
}

module rod_profile(h=1,s=1)
{
  scale([s,s,1])
  linear_extrude(height = h, center = true, convexity = 10, scale=1)
    contour();
}

module clamp(size=1,height=10)
{
  difference()
  {
    scale([1.1*size,size,1])
    cylinder(d=30,h=height,$fn=64,center=true);
    scale([size,size,1])
    translate(rod_pos)
      rod_profile(h=height+1,s=1);
  }
}

module print_clamp_half(i=1,size=1,height=10)
{
  difference()
  {
    rotate(clamp_rot)
    clamp(size,height);
    translate([0,i*50,0])
      cube([100,100,height+1],center=true);
    for(j=[-1,1])
    translate([j*13.5*size,0,0])
    if(i > 0)
    rotate([90,0,0])
    {
      translate([0,0,-0.1])
      cylinder(d=3,h=100,$fn=12,center=false);
      translate([0,0,4])
      cylinder(d=6,h=100,$fn=12,center=false);
    }
    else
      rotate([-90,0,0])
        translate([0,0,-0.1])
        cylinder(d=1.8,h=7,$fn=12,center=false);
  }
}

/*
//size = 1.0; // small
size = 1.2; // middle
for(i=[-1,1])
  translate([0,-i])
     print_clamp_half(i,size);
*/