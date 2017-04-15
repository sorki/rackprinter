from __future__ import division

from solid import *
from solid.utils import *

import sys
sys.path.insert(0, '/home/rmarko/hs/pycad/lib') # c(ad) lib
sys.path.insert(0, '/home/rmarko/hs/pycad/') # SolidMcad
import c
from c import *

from rc import bat, control, powerdist, spacer, stack
from rc import rotor

import random

from config import *
from profile import profile2020_smooth
from carriage import *

from SolidMcad import nuts_and_bolts

META = {
    'model': 'rackprinter',
    'author': 'Richard Marko',
    'date': '2017-01-10',
    'segments': segments,
}

def rail(x=10, y=500, z=10, wall=1):
    w = wall
    o = cube([x, y, z], center=True)
    o -= cube([x - w, y + w, z - w], center=True)
    return o

def rack():
    o = cube([rack_x, rack_y, rack_z], center=True)
    o -= back(wall)(cube([rack_x - wall, rack_y, rack_z - wall], center=True))
    # dekel
    o -= up(rack_z/2.)(cube([200, 400, rack_z], True))
    return o


def yaxis(yoff=0):
    # rails
    off = (x_axis_len/2. + carriage_z_bound)
    r = rotate([90, 0, 0])(profile2020_smooth(height=y_axis_len))
    o = left(off)(r)
    o += right(off)(r)

    # carriages
    l = carriage_x
    xoff = x_axis_len/2.
    for i in [-1, 1]:
        o += translate([i * (xoff), yoff, 0])(
                rotate([90, 0, i*90])(carriage(l, carriage_y, carriage_z)))

    return o

def xaxis():
    # rail
    r = rotate([0, 90, 0])(profile2020_smooth(height=x_axis_len))
    o = back(10)(r) + fwd(10)(r)

    # carriage
    yoff = - 10 - carriage_z_bound
    for i in [-1, 1]:
        xoff = random.randint(-100, 100)
        o += translate([xoff, i*yoff, 0])(
                rotate([i*90, 0, 180])(carriage(carriage_x, carriage_y, carriage_z))) 
    return o

def lmh16l():
    l = 70
    d = 16
    d_out = 28
    d_flange = 48
    h = 6
    k = 34
    d_hole = 4.5
    d_hole2 = 8
    h_hole2 = 4.4
    b = 31/2.
    c = 22/2.

    o = cylinder(r=d_out/2., h=l)
    o -= up(-1)(cylinder(r=d/2., h=l+2))
    o += intersection()([
            cylinder(r=d_flange/2., h=h)
          , cube([k, k*10, h*10], center=True)])

    hole = debug(cylinder(r=d_hole/2., h=h) + cylinder(r=d_hole2/2., h=h_hole2))

    for i in [-1, 1]:
        for j in [-1, 1]:
            o -= translate([i * c, j * b, 0])(hole)

    return up(l)(rotate([180, 0, 0])(o))

def vrail(h=vrail_h):
    o = cylinder(r=vrail_d/2., h=h)
    return o

def bed():
    bx = bed_support_x_off
    bz = bed_support_z_off
    by = bed_support_y_off

    # surface
    o = up(10 + bz + bed_surface_h/2)(cube([bed_x, bed_y, bed_surface_h], center=True))

    # test obj
    o += up(20 + bz + bed_surface_h/2)(color(red)(cube([20, 20, 20],
        center=True)))

    # supports
    pl = bed_x + bed_support_x_off
    r = rotate([0, 90, 0])(profile2020_smooth(height=pl))

    pll = bed_y - bx
    r_long = rotate([90, 0, 0])(profile2020_smooth(height=pll))

    for i in [-1, 1]:
        o += up(bz)(fwd(i*by)(r))

    for i in [-1, 1]:
        o += up(bz)(right(i*bed_x/2.)(r_long))

    # rails
    xoff = rack_x/2. - vrail_x_off
    yoff = rack_y/2. - vrail_y_off
    for j in [-1, 1]:
        for i in [-1, 1]:
            o += translate([i*xoff, j*yoff, 0])(vrail())

            # bearings
            o += translate([i*xoff, j*yoff, 20])(lmh16l())


    o = down(bed_down)(o)
    return o

def printer():
    ypos = random.randint(-200, 200)

    o = union()([
        up(gantry_up)(yaxis(ypos)),
        translate([0, ypos, gantry_up])(xaxis()),
        down(100)(bed()),
        ])

    o = up(200)(o)
    return o

def rackprinter():

    return union()([
        rack(),
        (rack()),
        printer(),
    ])


if __name__ == "__main__":
    out = rackprinter()
    #out = left(0)(mystack())
    scad_render_to_file(out,
                        filepath='{0}.scad'.format(META['model']),
                        file_header='$fn = %s;' % META['segments'],
                        include_orig_code=False)
