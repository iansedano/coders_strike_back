"""
Coders Strike back Gold League Bot.

Currently standing in at around 960th place in gold league.

cp = cp
rel = relation
agl = angle
d = d


"""
import sys
import math
import numpy as np

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


def get_signed_angle(a1, a2):

    diff = a1 - a2
    if diff > pi:
        diff -= pi*2
    if diff < -pi:
        diff += pi*2

    return diff


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
    global_x_to_cp = cp_rel['x'] - pod['x']
    global_y_to_cp = cp_rel['y'] - pod['y']

    # d to cp
    cp_rel['d'] = math.hypot(
        global_x_to_cp,
        global_y_to_cp)

    # print(f"d_to_cp {int(d_to_cp)}",
    #       file=sys.stderr)

    quadrant = quad_from_pos(cp['x'], cp['y'], pod['x'], pod['y'])

    x_to_cp = 0  # initalizing TODO deal with 0 values
    y_to_cp = 0  # initalizing TODO deal with 0 values

    if quadrant == 1:
        x_to_cp = cp['x'] - pod['x']
        y_to_cp = pod['y'] - cp['y']
    elif quadrant == 2:
        x_to_cp = (pod['x'] - cp['x']) * -1
        y_to_cp = pod['y'] - cp['y']
    elif quadrant == 3:
        x_to_cp = (pod['x'] - cp['x']) * -1
        y_to_cp = (cp['y'] - pod['y']) * -1
    elif quadrant == 4:
        x_to_cp = cp['x'] - pod['x']
        y_to_cp = (cp['y'] - pod['y']) * -1

    # getting the absolute angle of the cp from the pods position
    cp_rel['abs_angle'] = math.atan2(
        y_to_cp, x_to_cp)

    cp_rel['facing_offset'] = get_signed_angle(
        cp_rel['abs_angle'], pod['angle_facing']
        )

    cp_rel['heading_offset'] = get_signed_angle(
        cp_rel['abs_angle'], pod['actual_heading_angle']
        )

    return cp_rel


def add_compensation_angle_info(cp_rel, pod):
    """
    Add compensation turning angle to the cp dictionary.

    With the d to cp, and the current vector
    heading offset, i.e. if the heading offset was 0, then
    the pod vector would be on perfect collision course with
    the target. Assuming that function is called when heading
    offset is > 0. Imagine drawing a line from pod to target,
    then draw a line from pod that is perpendicular to the
    last line. The projection of the vector will meet this
    perpendicular line to form a right angled triangle. This
    meeting point is how far the current vector will overshoot
    the target.

    Use the properties of this triangle to produce a compensation to the
    normal heading (x, y)
    """

    # how far the current heading will miss the target
    overshoot_d = abs(
        cp_rel['d'] * math.tan(
            abs(cp_rel['heading_offset'])
        )
    )
    # print(f"overshoot_d {overshoot_d}", file=sys.stderr)

    # the d between pod and the overshoot point.
    projection_pod_vector_d = math.hypot(
        cp_rel['d'], overshoot_d
    )

    # print(f"projection_pod_vector_d {projection_pod_vector_d}",
    #      file=sys.stderr)

    # coordinates of overshoot relative to pod

    x_overshoot = (projection_pod_vector_d *
                   math.cos(pod['actual_heading_angle']))
    y_overshoot = (projection_pod_vector_d *
                   math.sin(pod['actual_heading_angle']))

    # absolute values
    global_x_overshoot = (pod['x'] + x_overshoot)
    global_y_overshoot = (pod['y'] - y_overshoot)

    # d between overshoot point and taget
    global_x_cp_overshoot = (global_x_overshoot - cp_rel['x'])
    global_y_cp_overshoot = (global_y_overshoot - cp_rel['y'])

    # compensation values (point opposite target from overshoot)
    cp_rel['x_compensation'] = max(
                               min(int(-global_x_cp_overshoot), 1200), -1200)
    cp_rel['y_compensation'] = max(
                               min(int(-global_y_cp_overshoot), 1200), -1200)


def get_angle_to_next_cp(current_cp_rel, next_cp_rel, pod):
    """
    Calculate where to aim to cut corner without missing target.

    Using the cp after the current target, calculate where
    in the current target, the pod should aim, so as to corner efficiently.
    Return an x and y coordinate.

    """
    x_between_current_and_next_cp = (
        current_cp_rel['x'] - next_cp_rel['x'])
    y_between_current_and_next_cp = (
        current_cp_rel['y'] - next_cp_rel['y'])

    d_between_current_and_next_cp = math.hypot(
        x_between_current_and_next_cp,
        y_between_current_and_next_cp
    )

    # print(f"d_between_target_and_next_cp",
    # "{d_between_target_and_next_cp}", file=sys.stderr)

    x_between_pod_and_next_cp = next_cp_rel['x'] - pod['x']
    y_between_pod_and_next_cp = next_cp_rel['y'] - pod['y']

    d_between_pod_and_next_cp = math.hypot(
        x_between_pod_and_next_cp,
        y_between_pod_and_next_cp)

    # print(f"d_between_pod_and_next_cp",
    # f"{d_between_pod_and_next_cp}", file=sys.stderr)

    # law of cosines
    pod['angle_pod_current_next'] = math.acos(
        (
            d_between_pod_and_next_cp ** 2 -
            current_cp_rel['d'] ** 2 -
            d_between_current_and_next_cp ** 2
        ) / (
            -2 * current_cp_rel['d'] *
            d_between_current_and_next_cp
        )
    )


def get_corner_cut(pod):
    # +++++ current TARGET COMP +++++

    # form a triangle between the pod, the target and the next cp
    # Then draw a line from the target towards the line formed between the pod
    # and the next cp. The line from the target should form a
    # right angle on the line from pod and next ckpoint.
    # The point where these lines meet, where the right angle is formed,
    # I will call 'c'

    angle_current_pod_next = math.asin(
        (d_between_current_and_next_cp *
         math.sin(angle_pod_current_next)) /
        (d_between_pod_and_next_cp)
    )

    d_between_pod_and_c = (
        current_cp_rel['d'] *
        math.cos(angle_current_pod_next)
    )

    coeff_d_pod_c_and_pod_current = (
        d_between_pod_and_c /
        d_between_pod_and_next_cp
    )

    x_between_pod_and_c = (
        x_between_pod_and_next_cp *
        coeff_d_pod_c_and_pod_current
    )
    y_between_pod_and_c = (
        y_between_pod_and_next_cp *
        coeff_d_pod_c_and_pod_current
    )

    global_cx = pod['x'] + x_between_pod_and_c
    global_cy = pod['y'] + y_between_pod_and_c

    x_between_current_and_c = global_cx - current_cp_rel['x']
    y_between_current_and_c = global_cy - current_cp_rel['y']

    # print(f"x_between_current_and_c {x_between_current_and_c}",
    # file=sys.stderr)
    # print(f"y_between_current_and_c {y_between_current_and_c}",
    # file=sys.stderr)

    offset_from_current_center = 1100

    coeff_for_corner = (
        (offset_from_current_center ** 2) /
        (
            x_between_current_and_c ** 2 +
            y_between_current_and_c ** 2
        )
    )

    comp_x_current_c = x_between_current_and_c * coeff_for_corner
    comp_y_current_c = y_between_current_and_c * coeff_for_corner

    return {'x': comp_x_current_c, 'y': comp_y_current_c}

    # print(f"comp_x_target_c {comp_x_target_c}", file=sys.stderr)
    # print(f"comp_y_target_c {comp_y_target_c}", file=sys.stderr)


def set_next_cp_compensation_heading(pod):
    add_compensation_angle_info(pod['next_cp_rel'], pod)
    # add_compensation_angle_info(next_cp, pod)
    pod['heading_x'] = (
        pod['next_cp_rel']['x'] +
        pod['next_cp_rel']['x_compensation'])
    pod['heading_y'] = (
        pod['next_cp_rel']['y'] +
        pod['next_cp_rel']['y_compensation'])


def corner(pod):

    time_to_target = (
            pod['current_cp_rel']['d'] /
            pod['abs_velocity']
        )
    # print(f"time_to_target {time_to_target}", file=sys.stderr)
    get_angle_to_next_cp(pod['current_cp_rel'],
                         pod['next_cp_rel'], pod)

    if abs(pod['angle_pod_current_next']) > pi * 4/5:
        print(f"full speed", file=sys.stderr)
        if time_to_target < 6:
            set_next_cp_compensation_heading(pod)
            pod['thrust'] = 100

    elif abs(pod['angle_pod_current_next']) > pi * 3/5:
        print(f"soft", file=sys.stderr)
        if time_to_target < 5.65:
            set_next_cp_compensation_heading(pod)
            pod['thrust'] = 100

    elif abs(pod['angle_pod_current_next']) > pi * 2/5:
        print(f"90", file=sys.stderr)
        if time_to_target < 5:
            set_next_cp_compensation_heading(pod)
            pod['thrust'] = 80

    elif abs(pod['angle_pod_current_next']) > pi * 1/5:
        print(f"hard", file=sys.stderr)
        pod['heading_x'] += pod['current_cp_rel']['x_compensation']
        pod['heading_y'] += pod['current_cp_rel']['y_compensation']
        if time_to_target < 5.85:
            set_next_cp_compensation_heading(pod)
            pod['thrust'] = 20

    elif abs(pod['angle_pod_current_next']) < pi * 1/5:
        print(f"hairpin", file=sys.stderr)
        pod['heading_x'] += pod['current_cp_rel']['x_compensation']
        pod['heading_y'] += pod['current_cp_rel']['y_compensation']
        if time_to_target < 5.8:
            set_next_cp_compensation_heading(pod)
            pod['thrust'] = 10


def facing_compensation(pod):

    if abs(pod['current_cp_rel']['facing_offset']) > pi * 4/5:
        pod['thrust'] = 20

    elif abs(pod['current_cp_rel']['facing_offset']) > pi * 3/5:
        pod['thrust'] = 30


def get_heading(pod):

    pod['heading_x'] = pod['current_cp']['x']
    pod['heading_y'] = pod['current_cp']['y']

    pod['thrust'] = 100

    if (
            pod['current_cp_rel']['d'] > 4000 and
            pod['next_cp_rel']['heading_offset'] < 1):
        pod['thrust'] = "BOOST"

    # heading_x += int(corner_cut_x)
    # heading_y += int(corner_cut_y)

    if abs(pod['current_cp_rel']['heading_offset']) > 0.05:
        pod['heading_x'] += pod['current_cp_rel']['x_compensation']
        pod['heading_y'] += pod['current_cp_rel']['y_compensation']

    # CORNERING

    print(f"d{round(pod['current_cp_rel']['d'], 5)}", file=sys.stderr)
    print(f"actual_heading_angle {pod['actual_heading_angle']}  abs angle {pod['current_cp_rel']['abs_angle']}",
          file=sys.stderr)
    print(f"heading offset{round(pod['current_cp_rel']['heading_offset'], 5)}", file=sys.stderr)

    if (
            pod['abs_velocity'] > 0 and
            abs(pod['current_cp_rel']['heading_offset']) < 1):

        corner(pod)

    facing_compensation(pod)


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

    # VECTORS
    # getting the quadrant the vector is facing
    pod['vector_quad'] = quad_from_vector(pod['vx'], pod['vy'])

    # getting the absolute magnitude of pod vector
    pod['abs_velocity'] = math.hypot(pod['vx'], pod['vy'])

    # print(f" abs_velocity {int(pod['abs_velocity'])}", file=sys.stderr)

    pod['current_cp_rel'] = get_cp_rel_info(pod['current_cp'], pod)

    add_compensation_angle_info(pod['current_cp_rel'], pod)

    # ++++++++++++++++ANGLE TO current cp+++++++++++++++++++++

    pod['next_cp_rel'] = get_cp_rel_info(pod['next_cp'], pod)

    # corner_cut = get_angle_to_next_cp(
    #    pod['current_cp_rel'], pod['next_cp_rel'], pod
    #    )

    # pod['corner_cut_x'] = corner_cut['x']
    # pod['corner_cut_y'] = corner_cut['y']

    # +++++++++++++d FROM last +++++++++++++++

    pod['d_last_cp'] = math.hypot(
        (pod['x'] - pod['last_cp']['x']),
        (pod['y'] - pod['last_cp']['y']))

    get_heading(pod)

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

        # print(f" i:{i} current cp {current_cp_id} "
        #       f"angle facing:{angle_facing_in_rads} "
        #       f"x:{x}  y:{y} global_vx:{global_vx}  global_vy:{global_vy}",
        #       file=sys.stderr)

        pod[i]['x'] = x
        pod[i]['y'] = y
        pod[i]['global_vx'] = global_vx
        pod[i]['global_vy'] = global_vy
        pod[i]['angle_facing'] = angle_facing_in_rads
        pod[i]['current_cp'] = cps[current_cp_id]

        get_info(pod[i])
        # print(f"{pod[i]}", file=sys.stderr)

    for i in range(2):
        # OPPONENT
        x_2, y_2, global_vx_2, global_vy_2, angle_2, current_check_point_id_2 = [
            int(j) for j in input().split()]

    print(f"{pod[0]['heading_x']} {pod[0]['heading_y']} {pod[0]['thrust']}")
    print(f"{pod[1]['heading_x']} {pod[1]['heading_y']} {pod[1]['thrust']}")
