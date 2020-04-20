# preamble for Nomad machine
PREAMBLE = '''%
(BEGIN SETUP)
G90 (absolute coordinates)
G17 (XY plane)
G21 (work in mm)
G28 G91 Z0 (go to home pos; relative coords; height 0 = tool all the way up)
G90 (absolute coordinates)
G54 (work coordinate system)
(END SETUP)
'''

# conclusion for most G-Code programs
CONCLUSION = '''(PROGRAM FINISHED)
M30
%
'''

# command for spindle off
SPINDLE_OFF = 'M5'

# return a G-Code block for a tool change
def tool_change(tool_no):
    return 'T{:d} M6'.format(tool_no)

# return a G-Code block for turning the spindle on at a given RPM
def spindle_on(speed_rpm):
    return 'S{:d} M3'.format(speed_rpm)

# round to have 3 digits after decimal (more than that usually exceeds
# machine precision)!
def round3(x):
    return round(x, 3)

# linear or rapid motion
#
# parameters (all optional):
#
#  mtype:    motion type. 'rapid' or 'linear'
#
#  x, y, z:  destination coordinates of move
#
#  feedrate: feedrate (mm/min)
#
# returns a G-Code block for these parameters
def motion(mtype=None, x=None, y=None, z=None, feedrate=None):

    assert mtype in [None, 'rapid', 'linear']

    block = []

    if mtype == 'rapid':
        block.append('G0')
        if feedrate is not None:
            print('warning: feed rate will not affect rapid motion')
    elif mtype == 'linear':
        block.append('G1')
        if feedrate is None:
            print('warning: linear motion without feedrate!')

    for dim, meas in [('X', x), ('Y', y), ('Z', z)]:
        if meas is not None:
            block.append('{}{:g}'.format(dim, round3(meas)))

    if feedrate is not None:
        block.append('F{:g}'.format(round3(feedrate)))

    return ' '.join(block)

# clockwise or counterclockwise arc
#
# parameters:
#
#   turn: turn direction, 'cw' for clockwise, 'ccw' for counterclockwise
#
#   x, y: destination point of the arc
#
#   x_ctr_offs, y_ctr_offs: offset to center of arc from current point
#
#   z (optional): final z position of arc
#
# note that the distance between (x, y) and the current point
# should be the same as the length of the vector (x_ctr_offs, y_ctr_offs)
# as both correspond to the arc radius

def arc(turn, x, y, x_ctr_offs, y_ctr_offs, z=None, feedrate=None):

    assert turn in ['cw', 2, 'ccw']

    if turn == 'cw' or turn == 2:
        block = ['G2']
    else:
        block = ['G3']

    block.append('X{:g} Y{:g} I{:g} J{:g}'.format(
        round3(x), round3(y),
        round3(x_ctr_offs), round3(y_ctr_offs)))

    if z is not None:
        block.append('Z{:g}'.format(round3(z)))

    if feedrate is not None:
        block.append('F{:g}'.format(round3(feedrate)))

    return ' '.join(block)

