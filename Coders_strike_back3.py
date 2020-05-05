"""Hello"""

import sys
import math
import numpy as np


driving_matrix = [
{'a': 0, 'x': 10, 'y': 0},
{'i':1, 'a': 0.31831, 'x': 9.49766, 'y': 3.12962},
{'i':2, 'a': 0.63662, 'x': 8.0411, 'y': 5.94481},
{'i':3, 'a': 0.95493, 'x': 5.77666, 'y': 8.16273},
{'i':4, 'a': 1.27324, 'x': 2.93185, 'y': 9.56056},
{'i':5, 'a': 1.59155, 'x': -0.20752, 'y': 9.99785},
{'i':6, 'a': 1.90986, 'x': -3.32604, 'y': 9.43067},
{'i':7, 'a': 2.22817, 'x': -6.11039, 'y': 7.916},
{'i':8, 'a': 2.54648, 'x': -8.28085, 'y': 5.60603},
{'i':9, 'a': 2.86479, 'x': -9.61934, 'y': 2.73282},
{'i':10, 'a': 3.1831, 'x': -9.99139, 'y': -0.41494},
{'i':11, 'a': 3.14159, 'x': -10, 'y': 0},
{'i':12, 'a': -0.31831, 'x': 9.49766, 'y': -3.12962},
{'i':13, 'a': -0.63662, 'x': 8.0411, 'y': -5.94481},
{'i':14, 'a': -0.95493, 'x': 5.77666, 'y': -8.16273},
{'i':15, 'a': -1.27324, 'x': 2.93185, 'y': -9.56056},
{'i':16, 'a': -1.59155, 'x': -0.20752, 'y': -9.99785},
{'i':17, 'a': -1.90986, 'x': -3.32604, 'y': -9.43067},
{'i':18, 'a': -2.22817, 'x': -6.11039, 'y': -7.916},
{'i':19, 'a': -2.54648, 'x': -8.28085, 'y': -5.60603},
{'i':20, 'a': -2.86479, 'x': -9.61934, 'y': -2.73282},
{'i':21, 'a': -3.1831, 'x': -9.99139, 'y': 0.41494},
{'i':22, 'a': -3.14159, 'x': -10, 'y': 0}
]
angles = list(x['a'] for x in driving_matrix)

def get_heading(pod):

    if pod['current_cp_rel']['heading_offset'] > 0.1 and pod['abs_velocity'] > 20:

        pod['actual_heading_angle']
        closest_angle = min(
            angles, key = lambda x: abs(x - pod['actual_heading_angle'])
        )

        index_closest_angle = angles.index(closest_angle)

        abs_angle_to_target = 3.1

        diff = (pod['current_cp_rel']['abs_angle'] -
                pod['actual_heading_angle']) % 3.14159 - 3.14159

        how_many_turns = int(diff / 0.31831)


        pod_offset_x = int(
            driving_matrix[index_closest_angle + how_many_turns]['x']
            )
        pod_offset_y = int(
            driving_matrix[index_closest_angle + how_many_turns]['y']
            )

        global_x = pod['x'] + pod_offset_x
        global_y = pod['y'] + pod_offset_y

        pod['heading_x'] = global_x
        pod['heading_y'] = global_y

    else:
        pod['heading_x'] = pod['current_cp_rel']['x']
        pod['heading_y'] = pod['current_cp_rel']['y']

"""
Coders Strike back Gold League Bot.

Currently standing in at around 960th place in gold league.

cp = cp
rel = relation
agl = angle
d = d


"""




pi = 3.14159



# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++FUNCTIONS++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def constrain(val, min_val, max_val):
    """Constrain value between min and max."""
    return min(max_val, max(min_val, val))


def quad_from_pos(target_x, target_y, x, y):
    """Get the target quadrant from an x and y position."""
    if target_x > x and target_y < y:
        return 1
    elif target_x < x and target_y < y:
        return 2
    elif target_x < x and target_y > y:
        return 3
    elif target_x > x and target_y > y:
        return 4


def quad_from_vector(global_vx, global_vy):
    """Get the quadrant a vector is facing."""
    if global_vx > 0 and global_vy > 0:
        return 1
    elif global_vx < 0 and global_vy > 0:
        return 2
    elif global_vx < 0 and global_vy < 0:
        return 3
    elif global_vx > 0 and global_vy < 0:
        return 4


def get_cp_rel_info(cp, pod):
    """
    Return dictionary with cp info.

    Return a dictionay with information relating
    to cp and pod.
    """

    cp_rel = {}

    cp_rel['x'] = cp['x']
    cp_rel['y'] = cp['y']

    # x and y from pod to cp
    cp_rel['global_x_to_cp'] = cp_rel['x'] - pod['x']
    cp_rel['global_y_to_cp'] = cp_rel['y'] - pod['y']

    # d to cp
    cp_rel['d'] = math.hypot(
        cp_rel['global_x_to_cp'],
        cp_rel['global_y_to_cp'])

    # print(f"d_to_cp {int(d_to_cp)}",
    #       file=sys.stderr)

    cp_rel['quadrant'] = quad_from_pos(cp['x'], cp['y'], pod['x'], pod['y'])

    cp_rel['x_to_cp'] = 0  # initalizing TODO deal with 0 values
    cp_rel['y_to_cp'] = 0  # initalizing TODO deal with 0 values

    if cp_rel['quadrant'] == 1:
        cp_rel['x_to_cp'] = cp['x'] - pod['x']
        cp_rel['y_to_cp'] = pod['y'] - cp['y']
    elif cp_rel['quadrant'] == 2:
        cp_rel['x_to_cp'] = (pod['x'] - cp['x']) * -1
        cp_rel['y_to_cp'] = pod['y'] - cp['y']
    elif cp_rel['quadrant'] == 3:
        cp_rel['x_to_cp'] = (pod['x'] - cp['x']) * -1
        cp_rel['y_to_cp'] = (cp['y'] - pod['y']) * -1
    elif cp_rel['quadrant'] == 4:
        cp_rel['x_to_cp'] = cp['x'] - pod['x']
        cp_rel['y_to_cp'] = (cp['y'] - pod['y']) * -1

    # getting the absolute angle of the cp from the pods position
    cp_rel['abs_angle'] = math.atan2(
        cp_rel['y_to_cp'], cp_rel['x_to_cp'])

    cp_rel['facing_offset'] = (
        (cp_rel['abs_angle'] - pod['angle_facing']) +
        (pi / 2)) % pi - (pi / 2)
    cp_rel['heading_offset'] = (
        (cp_rel['abs_angle'] - pod['actual_heading_angle']) +
        (pi / 2)) % pi - (pi / 2)

    return cp_rel


def get_info(pod):
    """Get info relating to pod."""
    # Establishing target cp

    angle_facing_in_rads = pod['angle_facing']

    pod['next_cp'] = cps[(current_cp_id + 1) % (cp_count)]
    pod['last_cp'] = cps[(current_cp_id - 1) % (cp_count)]

    # translating global velocity as given to velocity relative to pod (0,0)
    pod['vx'] = pod['global_vx']
    pod['vy'] = pod['global_vy'] * -1

    # getting the angle of the pods direction calculated from vector
    pod['actual_heading_angle'] = (
        math.atan2(pod['vy'], pod['vx'])
    )  # TODO deal with zero values

    # getting the quadrant the vector is facing
    pod['vector_quad'] = quad_from_vector(pod['vx'], pod['vy'])

    # getting the absolute magnitude of pod vector
    pod['abs_velocity'] = math.hypot(pod['vx'], pod['vy'])

    print(f" abs_velocity {int(pod['abs_velocity'])}", file=sys.stderr)

    pod['current_cp_rel'] = get_cp_rel_info(pod['current_cp'], pod)

    facing_offset = (
            (pod['current_cp_rel']['abs_angle'] -
             pod['angle_facing'] + (pi / 2)
        ) % pi - (pi / 2)
    )
    heading_offset = (
        (
            (pod['current_cp_rel']['abs_angle'] -
             pod['actual_heading_angle']) + (pi / 2)
        ) % pi - (pi / 2)
    )


    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++HEADING ALGORITHM+++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



    get_heading(pod)

    thrust = 100

    if abs(facing_offset) > 1.5:
        thrust = 20
    elif abs(facing_offset) > 0.7:
        thrust = 90
    else:
        thrust = 100

    #heading_x += int(corner_cut_x)
    #heading_y += int(corner_cut_y)




    if pod['abs_velocity'] > 0:
        time_to_target = (
            pod['current_cp_rel']['d'] /
            pod['abs_velocity']
        )
        # print(f"time_to_target {time_to_target}", file=sys.stderr)

        if time_to_target < 5 and heading_offset < 0.9:
            
            pod['next_cp_rel'] = get_cp_rel_info(pod['next_cp'], pod)

            thrust = 0
            # add_compensation_angle_info(next_cp, pod)
            heading_x = pod['next_cp_rel']['x']
            heading_y = pod['next_cp_rel']['y']

            pod['heading_x'] = heading_x
            pod['heading_y'] = heading_y


    
    pod['thrust'] = thrust





# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++GAME LOOP++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

pod = {
    0: {},
    1: {},
    2: {},
    3: {}
}

laps = int(input())
cp_count = int(input())

cps = {}
for i in range(cp_count):
    cp_x, cp_y = [int(j) for j in input().split()]
#    print(f"{cp_x}", file=sys.stderr)
    cps[i] = {'x': cp_x, 'y': cp_y}

# print(f"cp count {cp_count}", file=sys.stderr)
# print(f"test {cps[1]['x']}", file=sys.stderr)

counter = 0


while True:
    counter += 1
    for i in range(2):

        x, y, global_vx, global_vy, angle_facing, current_cp_id = [
            int(j) for j in input().split()]

        # change to counter clockwise angle
        angle_facing = (-angle_facing) % 360
        # change to scale -180 0 180
        # (original angle seems to be off by 5 degrees,
        # hence the -175 instead of 180)
        angle_facing = (angle_facing - 175) % 360 - 180
        angle_facing_in_rads = angle_facing * (pi / 180)

        print(f" i:{i} current cp {current_cp_id} "
              f"angle facing:{angle_facing_in_rads} "
              f"x:{x}  y:{y} global_vx:{global_vx}  global_vy:{global_vy}",
              file=sys.stderr)

        pod[i]['x'] = x
        pod[i]['y'] = y
        pod[i]['global_vx'] = global_vx
        pod[i]['global_vy'] = global_vy
        pod[i]['angle_facing'] = angle_facing_in_rads
        pod[i]['current_cp'] = cps[current_cp_id]

        get_info(pod[i])
        print(f"{pod[i]}", file=sys.stderr)

    for i in range(2):
        # OPPONENT
        x_2, y_2, global_vx_2, global_vy_2, angle_2, current_check_point_id_2 = [
            int(j) for j in input().split()]

    print(f"{pod[0]['heading_x']} {pod[0]['heading_y']} {pod[0]['thrust']}")
    print(f"{pod[1]['heading_x']} {pod[1]['heading_y']} {pod[1]['thrust']}")
