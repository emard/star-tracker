/* all measures in mm */
// 0.8mm nozzle 0.3mm layer
include <nut_cutter.scad>

/* todo:
** [x] dent holes must be aligned, not dents
** [x] narrower and smaller big dents
** [x] intercusp strain release smaller, 0.1mm
** [x] remove intercuspidation
** [x] M3 thread: -0.15
** [x] M4 thread: -0.20, waterdrop
** [x] 30 mm mount holes M4
** [x] thread for M4
** [x] cut-snap 2 piece
** [x] subtract cube, leave only lower cut-snap
** [x] 2 screws M3 to tighten cut-snap
** [x] thread for M3
** [x] remove some dents - cannot assemble!!
*/

/* Z-extrusion height (vertical) enough to hold M3 screw hole */
zdim = 9;
/* X-length */
xdim = 29;
/* Y-width */
ydim = 29;

/* free space between parts */
freespace_big = 0.2;
freespace_small = 0.4;

/* number of small dents */
ndent1 = 40;
/* dent depth */
ddent1 = 0.0; // 0.5 default, 0 to disable
/* dent width large */
wdent1l = 0.8;
/* dent width small */
wdent1s = 0.3; 
/* big wheel radius (with dents d = 16.7mm)  */
rbig = (16.7+freespace_big)/2;
/* big wheel height */
zbig = 3.7;

/* number of big dents = half of small dents */
ndent2 = ndent1/2;
/* dent depth */
ddent2 = 0.5; // 0.5 default, 0.0 to disable
/* dent width large */
wdent2l = 0.8;
/* dent width small */
wdent2s = 0.3;
/* small wheel radius (with dents d = 13.0mm) */
rsmall = (13.0+freespace_small)/2;

/* make sure we cut it all */
overcut = 0.001;

/* mounting hole radius */
rmounthole = 1.9/2;
/* mounting holes distance */
dmounthole = 22;

/* tightening screws distance (B careful, do not intersect dents) */
dtighthole = 22;
/* let screw pass freely */
rM3free = (3+1)/2;
/* screw threadhole */
rM3thread = (3-0.0)/2;

/* intercuspidation Y center aligns with tightening hole */
ycuspcenter = dtighthole/2;
/* intercuspidation depth */
dcusp = 4;
/* intercuspidation small, big */
icusps = 4;
icuspb = 5;
freecusp = 0.1;

module droplet_profile(h, r, rotation) {
        union()
        {
          cylinder(h = h, r = r, $fa=360/16, $fs=0.5, center=true);
            rotate([0,0,rotation])
              linear_extrude(height = h, twist = 0, convexity = 2, center=true)
                polygon([
                 [ -r * sqrt(2)/2, r * sqrt(2)/2],
                 [              0, r * sqrt(2)],
                 [  r * sqrt(2)/2, r * sqrt(2)/2],
                 ]);
        }

}

module eye_profile(h, r, rotation) {
        union()
        {
          cylinder(h = h, r = r, $fa=360/16, $fs=0.5, center=true);
          rotate([0,0,rotation])
              linear_extrude(height = h, twist = 0, convexity = 2, center=true)
                polygon([
                 [ -r * sqrt(2)/2, r * sqrt(2)/2],
                 [              0, r * sqrt(2)],
                 [  r * sqrt(2)/2, r * sqrt(2)/2],
                 ]);
          rotate([0,0,180+rotation])
              linear_extrude(height = h, twist = 0, convexity = 2, center=true)
                polygon([
                 [ -r * sqrt(2)/2, r * sqrt(2)/2],
                 [              0, r * sqrt(2)],
                 [  r * sqrt(2)/2, r * sqrt(2)/2],
                 ]);
        }
}

module sprocket_adapter() {
delta=0.001;
union() {
  difference() {
    translate([0,0,zdim/2])
      cube([xdim, ydim, zdim], center=true);
    union() {
      translate([0,0,zbig/2])
          cylinder(h=zbig+delta, r=rbig, $fa=360/ndent1, $fs=0.5, center=true);
      translate([0,0,zdim/2])
          cylinder(h=zdim+delta, r=rsmall, $fa=360/ndent2, $fs=0.5, center=true);

      /* 2 holes for screws cca 30 mm apart */
      translate([-dmounthole/2,0,zdim/2])
        eye_profile(h = zdim + overcut, r = rmounthole, rotation = -90);
      translate([ dmounthole/2,0,zdim/2])
        eye_profile(h = zdim + overcut, r = rmounthole, rotation = 90);

      /* tightening M3 screw, larger in "removed" part */
      translate([0,-dtighthole/2,zdim/2])
        rotate([0,90,0])
          cylinder(d=2.7,h=xdim+overcut,$fn=16,center=true); // circular
          //eye_profile(h = xdim+overcut, r = rM3free, rotation = -90); // droplet shape

    translate([-xdim/2,-dtighthole/2,zdim/2])
      rotate([0,90,0])
         head_cutter(d=5,h=9);

      /* tightening M3 screw, with droplet shape, smaller/thread in "extended" part */
    translate([0,dtighthole/2,zdim/2])
      rotate([0,90,0])
        cylinder(d=2.0,h=xdim+overcut,$fn=16,center=true); // circular
          //eye_profile(h = xdim+overcut, r = rM3thread, rotation = -90); // droplet shape

      /* polygon cuts this in snap-on half */
      translate([0,0,-delta/2])
      linear_extrude(height = zdim+delta, twist = 0, convexity = 8)
        polygon([[ 0,               -ydim/2],
                 [ xdim,            -ydim/2],
                 [ xdim,             ydim/2],
                 [ 0,                ydim/2],
                 [ 0,                ycuspcenter+icusps/2],

/* intercuspidation removed */
/*
                 [ dcusp,            ycuspcenter+icuspb/2],
                 [ dcusp,            ycuspcenter-icuspb/2],
                 [ 0,                ycuspcenter-icusps/2],
                 [ 0,               -ycuspcenter+icusps/2+freecusp],
                 [-dcusp-freecusp,  -ycuspcenter+icuspb/2+freecusp],
                 [-dcusp-freecusp,  -ycuspcenter-icuspb/2-freecusp],
                 [ 0,               -ycuspcenter-icusps/2-freecusp]
*/
                 ]*(1+delta));

      /* cuts off upper notch for easier insertion */
      translate([dcusp/2,0,zbig/2])
        cube([dcusp,ydim,zbig], center = true);

      /* cut off corners */
      for(i=[-1:2:1])
      translate([-xdim/2,ydim*i*0.92,zdim/2])
        rotate([0,0,45])
          cube([xdim,ydim,zdim+delta],center=true);
    }
  }

      /* big radius, small dents */
      for(angle = [360/ndent1/2 : 360/ndent1 : 360])
        if(angle > 180-50 && angle < 180+50)
        rotate([0,0,angle])
          translate([rbig-ddent1/2,0,0])
          {
            linear_extrude(height = zbig, twist = 0, convexity = 2)
              polygon([[ ddent1/2,        -wdent1l/2],
                       [-ddent1/2,        -wdent1s/2],
                       [-ddent1/2,         wdent1s/2],
                       [ ddent1/2,         wdent1l/2]]);
          }

      /* small radius, big dents */
      for(angle = [360/ndent2/2 : 360/ndent2 : 360])
        if(angle > 180-30 && angle < 180+30)
        rotate([0,0,angle])
          translate([rsmall-ddent2/2,0,zbig])
          {
            linear_extrude(height = zdim-zbig, twist = 0, convexity = 2)
              polygon([[ ddent2/2,        -wdent2l/2],
                       [-ddent2/2,        -wdent2s/2],
                       [-ddent2/2,         wdent2s/2],
                       [ ddent2/2,         wdent2l/2]]);
          }
}

}

// printable position
if(1)
translate([0,0,xdim/2])
  rotate([0,-90,0])
    sprocket_adapter();

