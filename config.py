segments = 66
tol = 0.1

rack_x = 600
rack_y = 900
rack_z = 900
wall = 10

gantry_up = 100

bed_x = 400
bed_y = 800

bed_down = rack_z/2. + 66.6
bed_surface_h = 10

bed_support_x_off = 20
bed_support_z_off = 100
bed_support_y_off = 400

vrail_d = 16
vrail_h = 666
vrail_x_off = 60
vrail_y_off = 60

y_axis_len = rack_y
x_axis_len = rack_x - 70

carriage_x = 60
carriage_y = 50
carriage_z = 10
carriage_z_bound = 22

# random combinators
def lr(x): return(left(x), right(x))
