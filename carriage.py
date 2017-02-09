# Aleksandr Saechnikov 17 june 2015
# ported to SolidPython by Richard Marko, 2017

from solid import *
from solid.utils import *

import sys
sys.path.insert(0, '/home/rmarko/hs/pycad/lib') # c(ad) lib
sys.path.insert(0, '/home/rmarko/hs/pycad/') # SolidMcad
import c
from c import *

from SolidMcad.nuts_and_bolts import *
from config import *
from profile import profile2020_smooth

META = {
    'model': 'carriage',
    'author': 'Richard Marko',
    'date': '2017-01-10',
    'segments': 100,
}

def vwheel(r1=7, r2=11, h=4):
    o = down(h)(cylinder(r1=r1, r2=r2, h=h))
    o += up(h)(rotate([180, 0, 0])(cylinder(r1=r1, r2=r2, h=h)))
    o -= bolt_hole(3, 10, tol)
    return color(gray)(o)

def carriage(x=50, y=50, z=10):
    bh = 30
    xo = 15
    yo = 16 # don't touch this
    rot = 1 # and dis
    o = rounded(x, y, z)

    o += bg( up(22)(rotate([0, 90, 0])(profile2020_smooth(height = 50))) )

    hobj = debug( bolt_hole(3, bh, tol) )
    wheel = up(z + 12)(vwheel())
    for i in [-1, 1]:
        for j in [-1, 1]:
            o -= translate([i * xo, j * yo, -0.1])(hobj)
            o += bg( translate([i * xo, j * yo, -0.1])(wheel) )

        #o -= translate([i * xo, -yo, -0.1])(hobj)
        o -= debug(rotate([-rot, 0, 0])(translate([i * xo, -yo, 0])(hobj)))
    return o

if __name__ == "__main__":
    out = carriage()
    scad_render_to_file(out,
                        filepath='{0}.scad'.format(META['model']),
                        file_header='$fn = %s;' % META['segments'],
                        include_orig_code=False) 

