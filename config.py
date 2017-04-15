segments = 66
tol = 0.1

prof_w = 10

rack_x = 600
rack_y = 900
rack_z = 900

show_rack = False

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

y_axis_len = rack_y - 50
x_axis_len = rack_x - 80

y_axis_pulley_offset = 15

y_axis_secondar_belt_len = 60

carriage_x = 60
carriage_y = 50
carriage_z = 10
carriage_dist = 15
carriage_z_bound = prof_w + carriage_dist

# random combinators
def lr(x): return(left(x), right(x))
