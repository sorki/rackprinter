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

from config import *
from profile import profile2020_smooth
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

rack_x = 400
rack_y = 800
rack_z = 800
wall = 10
def rack():
    o = cube([rack_x, rack_y, rack_z], center=True)
    o -= back(wall)(cube([rack_x - wall, rack_y, rack_z - wall], center=True))
    return o

y_axis_len = rack_y
x_axis_len = rack_x - 20

def yaxis():
    r = rotate([90, 0, 0])(profile2020_smooth(height=y_axis_len))
    o = left(x_axis_len/2.)(r)
    o += right(x_axis_len/2.)(r)
    return o

def xaxis():
    r = rotate([0, 90, 0])(profile2020_smooth(height=x_axis_len))
    o = back(10)(r) + fwd(10)(r)
    return o

def rackprinter():
    return union()([
        bg(rack()),
        yaxis(),
        up(50)(xaxis()),
    ])


if __name__ == "__main__":
    out = rackprinter()
    #out = left(0)(mystack())
    scad_render_to_file(out,
                        filepath='{0}.scad'.format(META['model']),
                        file_header='$fn = %s;' % META['segments'],
                        include_orig_code=False)
