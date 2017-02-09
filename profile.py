# Aleksandr Saechnikov 17 june 2015
# ported to SolidPython by Richard Marko, 2017

from solid import *
from solid.utils import *

META = {
    'model': 'profile2020',
    'author': 'Richard Marko',
    'date': '2017-01-10',
    'segments': 100,
}

def profile2020(size=20, height=10):
    return down(height/2.)(linear_extrude(height=height)(
        union()([
            profile_part(size),
            rotate([0,0,90]) (profile_part(size)),
            rotate([0,0,180])(profile_part(size)),
            rotate([0,0,270])(profile_part(size)),
        ])
    ))


def profile_part(size=20):
    d = 5
    r = 1.5
    s1 = 1.8
    s2 = 2
    s3 = 6
    s4 = 6.2
    s5 = 9.5
    s6 = 10.6
    s7 = 20

    reSize = size/20

    k0 = 0
    k1 = d*0.5*cos(45)*reSize
    k2 = d*0.5*reSize
    k3 = ( (s7*0.5-s3)-s1*0.5*sqrt(2) )*reSize
    k4 = s4*0.5*reSize
    k5 = ( s7*0.5-s3 )*reSize
    k6 = s6*0.5*reSize
    k7 = ( s6*0.5+s1*0.5*sqrt(2) )*reSize
    k8 = ( s7*0.5-s2 )*reSize
    k9 = s5*0.5*reSize
    k10 = s7*0.5*reSize
    k10_1 = k10-r*(1-cos(45))*reSize
    k10_2 = k10-r*reSize

    return polygon(points=[
        [k1,k1],[k0,k2],[k0,k5],[k3,k5],
        [k6,k7],[k6,k8],[k4,k8],[k9,k10],
        [k10_2,k10],[k10_1,k10_1],
        [k10,k10_2],
        [k10,k9],[k8,k4],[k8,k6],[k7,k6],
        [k5,k3],[k5,k0],[k2,k0]
    ])


def profile2020_smooth(size=20, height=10):
    return down(height/2.)(linear_extrude(height=height)(
        difference()(
            union()([
                profile_part_smooth(size),
                rotate([0,0,90]) (profile_part_smooth(size)),
                rotate([0,0,180])(profile_part_smooth(size)),
                rotate([0,0,270])(profile_part_smooth(size)),
            ]),
            circle(r=size/20.*2.5)
        )
    ))

def profile_part_smooth(size=20):
    r_center = 0.5*size-1.5*size/20
    return union()([
        translate ([r_center,r_center])(circle(r=1.5*size/20)),
        profile_part(size)
    ])


if __name__ == "__main__":
    out = profile2020_smooth()
    scad_render_to_file(out,
                        filepath='{0}.scad'.format(META['model']),
                        file_header='$fn = %s;' % META['segments'],
                        include_orig_code=False) 

