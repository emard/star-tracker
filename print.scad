// LANG=hr_HR.UTF8 prusa-slicer
// 0,8 mm nozzle
// 0.6 mm layer


include <sprocket_adapter_0.8mm_nozzle.scad>
include <rod_holder.scad>

// screws inox tin
// 2x 2.2x6 mm
// 2x 2.2x9 mm
if(0)
  rotate([0,-90,0])
    sprocket_adapter();

if(1)
  rotate([0,0,0])
  rod_holder();