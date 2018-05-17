$fn=100;

bottleRadius = 15;
stopperRadius = 10;
lipThickness = 5;
thickness = 5;

module boss(position) {
    translate(position) {
        difference() {
            cylinder(r=4,h=thickness);
            cylinder(r=2.5,h=thickness);
        }
    }
}

bosses = [
    [-1*(bottleRadius+lipThickness),-5.7,0],
    [(bottleRadius+lipThickness),-5.7,0],
    [-1*(bottleRadius+lipThickness),5.7,0],
    [(bottleRadius+lipThickness),5.7,0]
];

union() {
    difference() {
        cylinder(r=bottleRadius+lipThickness,h=thickness);
        cylinder(r=stopperRadius,h=thickness);
        for (pos = bosses) {
            translate(pos) {
                cylinder(r=4,h=thickness);
            }
        }
    }
    for (pos = bosses) {
        boss(pos);
    }
}