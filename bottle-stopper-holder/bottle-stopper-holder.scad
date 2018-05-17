$fn=100;

bottleRadius = 15;
thickness = 5;
neckHeight = 20;

module tab () {
    wallThickness = 1.5;
    screwRadius = 2.5;
    tabThickness = 3;
    distance = 10;
    translate([0,-1*tabThickness,1]) {
        difference() {
            minkowski() {
                cube([distance+screwRadius+wallThickness-1, 1, 2*wallThickness+2*screwRadius-2]);
                translate([0,tabThickness-1,0]) {
                    rotate([90,0,0]) {
                        cylinder(r=1,h=tabThickness-1);
                    }
                }
            }
            translate([distance,tabThickness,screwRadius+wallThickness-1]) {
                rotate([90,0,0]) {
                        cylinder(h=tabThickness, r=screwRadius);
                }
            }
        }
    }
}

module tabs() {
    translate([bottleRadius+thickness-1,0,0]) {
        tab();
    }
    translate([bottleRadius+thickness-1,-3,7]) {
        cube([14,3,neckHeight-14]);
    }
    translate([bottleRadius+thickness-1,0,neckHeight-8]) {
        tab();
    }
}

module threadedInsert() {
    lambda=0.1;
    translate([0,0,-6.3]) {
        cylinder(r=4.83/2-lambda,h=1);
        translate([0,0,1]) {
            cylinder(r=5.2/2-lambda,h=1);
        }
        translate([0,0,2]) {
            cylinder(r=5.59/2-lambda,h=4.35);
        }
    }
}

union() {
    difference() {
        cylinder(r=bottleRadius+thickness, h=neckHeight);
        translate([-1*(bottleRadius+thickness),0,0]) {
            cube([2*(bottleRadius+thickness),bottleRadius+thickness,neckHeight]);
        }
        cylinder(r=bottleRadius, h=neckHeight);
        translate([bottleRadius+thickness,-5.7,0]) {
            cylinder(r=4,h=neckHeight);
        }
        translate([-1*(bottleRadius+thickness),-5.7,0]) {
            cylinder(r=4,h=neckHeight);
        }
    }
    translate([bottleRadius+thickness,-5.7,0]) {
        difference() {
            cylinder(r=4,h=neckHeight);
            translate([0,0,neckHeight]) {
                threadedInsert();
            }
        }
    }
    translate([-1*(bottleRadius+thickness),-5.7,0]) {
        difference() {
            cylinder(r=4,h=neckHeight);
            translate([0,0,neckHeight]) {
                threadedInsert();
            }
        }
    }
    tabs();
    translate([0,0,neckHeight]) {
        rotate([0,180,0]) {
            tabs();
        }
    }
}