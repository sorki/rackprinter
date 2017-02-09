from solid import *
from solid.utils import *

#import sys
#sys.path.insert(0, '/home/rmarko/hs/pycad/lib') # c(ad) lib
#sys.path.insert(0, '/home/rmarko/hs/pycad/') # SolidMcad
#import c
#from c import *

from config import *

META = {
    'model': 'test_cradle',
    'author': 'Richard Marko',
    'date': '2017-02-07',
    'segments': 200,
}


motor_r = 21.
motor_h = 33.
motor_r_mount  = 35.3/2
motor_h_mount  = 10.0
axis_r = 2.5
motor_axis_r = axis_r
axis_len = 79.6
axis_offset = 15.0
mount_dist = 8.7
motor_clearance_r = 6.0


def motor_mounting_holes(d=mount_dist, obj=cylinder(r=1.5, h=50)):
    h = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            h.append(translate([d*i, d*j, 0])(obj))

    h.append(cylinder(r=motor_clearance_r, h=50))
    return union()(h)

def motor():
    o = up(motor_h/2.)(cylinder(r=motor_r, h=motor_h, center=True))
    o += up(motor_h + motor_h_mount/2. + 1)(cylinder(r2=motor_r_mount, r1=motor_r, h=motor_h_mount, center=True))
    o += up(axis_len/2. - axis_offset)(cylinder(r=axis_r, h=axis_len, center=True))

    o -= motor_mounting_holes()

    return o

def motor_mount(h=5):
    o = cylinder(r=enc_r, h=h)
    o -= motor_mounting_holes(obj=cylinder(r=2.0, h=h*2))
    return o


enc_h = 35.55
enc_r = 19.0
enc_r2 = 10.0
enc_axis_r = 3.0
enc_axis_len = 52.44
enc_hole = 1.5
enc_hole_offset = 14.
enc_h2 = 5.0

def encoder_mounting_holes(d=enc_hole_offset, obj=cylinder(r=1.5, h=40)):
    h = []
    for i in [0, 1, 2]:
        h.append(rotate(120*i)(translate([d, 0, 0])(obj)))

    h.append(cylinder(r=enc_r2 + 0.1, h=40))
    return union()(h)

def encoder():
    o = up(enc_h/2.)(cylinder(r=enc_r, h=enc_h, center=True))

    smaller_h = enc_h + 5.
    o += up(smaller_h/2.)(cylinder(r=enc_r2, h=smaller_h, center=True))
    o += up(enc_axis_len/2.)(cylinder(r=enc_axis_r, h=enc_axis_len, center=True))

    o -= encoder_mounting_holes()

    return o

def encoder_mount(h=5):
    o = cylinder(r=enc_r, h=h)
    o -= encoder_mounting_holes(obj=cylinder(r=2.0, h=h*2))
    return o

def cradle():

    h = 5
    yo = 40
    zs = 30

    m = background( translate([0, 45, zs])(rotate([90, 0, 0])(motor())) )
    e = background( translate([0, -yo - 35, zs])(rotate([-90, 0, 0])(encoder())) )

    a = translate([0, 0, zs])(rotate([90, 0, 0])(motor_mount()))
    b = translate([0, -2, 1])(cube([50, 5, 2], center=True))

    c = translate([0, -yo, zs])(rotate([-90, 0, 0])(encoder_mount()))
    d = translate([0, -yo+2.5, 1])(cube([50, 5, 2], center=True))

    o = hull()(a, b)
    o -= translate([0, 1, zs])(rotate([90, 0, 0])(motor_mounting_holes()))

    o += hull()(c, d)
    o -= translate([0, -11, zs])(rotate([90, 0, 0])(encoder_mounting_holes()))

    o += translate([0, -yo/2, h/2.])(cube([50, yo, h], center=True))
    o += translate([0, -yo/2, h/2. + 10/2.])(cube([5, yo, 10], center=True))

    return  o + m + e


def coupler(a_r=motor_axis_r, b_r=enc_axis_r, r=5., h=20.):
    o = cylinder(r=r, h=h)

    # motor side
    tol = 0.30
    o -= up(-0.1)(cylinder(r=a_r + tol, h=h))
    o += debug( up(h/4.)(right(3)(cube([2, a_r*2, h/2.], center=True) )))

    # encoder side
    tol = 0.41
    o -= up(h/2. + 0.1)(cylinder(r=b_r + tol, h=h/2.))
    o += debug( up(h/2. + h/4)(right(3.3)(cube([1, a_r*2 - 1, h/2.], center=True) )))

    return o

def assembly():
    o = cradle()

    o += background( translate([0, -10, 30])(rotate([90, 0, 0])(coupler()) ))
    return o

if __name__ == "__main__":
    #out = cradle()
    #out = coupler()
    out = assembly()
    scad_render_to_file(out,
                        filepath='{0}.scad'.format(META['model']),
                        file_header='$fn = %s;' % META['segments'],
                        include_orig_code=False)
