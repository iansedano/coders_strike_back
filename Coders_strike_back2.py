"""
Coders Strike back Gold League Bot.

Currently standing in at around 960th place in gold league.

cp = cp
rel = relation
agl = angle
d = distance


"""
import sys
import math
import numpy as np

laps = int(input())
cp_count = int(input())

cps = {}
for i in range(cp_count):
    cp_x, cp_y = [int(j) for j in input().split()]
#    print(f"{cp_x}", file=sys.stderr)
    cps[i] = {'x': cp_x, 'y': cp_y}
cp_count
# print(f"cp count {cp_count}", file=sys.stderr)
# print(f"test {cps[1]['x']}", file=sys.stderr)

counter = 0

pi = 3.14159


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


def get_cp_info(cp_id, pod):
    """
    Return dictionary with cp info.

    Return a dictionay with information relating
    to cp and pod.
    """
    
    x = cps[cp_id]['x']
    y = cps[cp_id]['y']

    # x and y from pod to cp
    global_pod_to_cp_x = x - pod['x']
    global_pod_to_cp_y = y - pod['y']

    # distance to cp
    distance_to_cp = math.hypot(
        global_pod_to_cp_x,
        global_pod_to_cp_y)

    # print(f"distance_to_cp {int(distance_to_cp)}",
    #       file=sys.stderr)

    cp_quadrant = quad_from_pos(x, y, pod['x'], pod['y'])

    x_to_cp_from_pod = 0  # initalizing TODO deal with 0 values
    y_to_cp_from_pod = 0  # initalizing TODO deal with 0 values

    if cp_quadrant == 1:
        x_to_cp_from_pod = x - pod['x']
        y_to_cp_from_pod = pod['y'] - y
    elif cp_quadrant == 2:
        x_to_cp_from_pod = (pod['x'] - x) * -1
        y_to_cp_from_pod = pod['y'] - y
    elif cp_quadrant == 3:
        x_to_cp_from_pod = (pod['x'] - x) * -1
        y_to_cp_from_pod = (y - pod['y']) * -1
    elif cp_quadrant == 4:
        x_to_cp_from_pod = x - pod['x']
        y_to_cp_from_pod = (y - pod['y']) * -1

    # getting the absolute angle of the cp from the pods position
    abs_angle_to_cp = abs_angle_to_cp = math.atan2(
        y_to_cp_from_pod, x_to_cp_from_pod)

    facing_offset = (
        (abs_angle_to_cp - pod['angle_facing']) +
        (pi / 2)) % pi - (pi / 2)
    heading_offset = (
        (abs_angle_to_cp - pod['actual_heading_angle']) +
        (pi / 2)) % pi - (pi / 2)

    return{
        'x': x,
        'y': y,
        'distance_to_cp': distance_to_cp,
        'x_to_cp_from_pod': x_to_cp_from_pod,
        'y_to_cp_from_pod': y_to_cp_from_pod,
        'abs_angle_to_cp': abs_angle_to_cp,
        'cp_quadrant': cp_quadrant,
        'facing_offset': facing_offset,
        'heading_offset': heading_offset
    }


def add_compensation_angle_info(cp_info_dict, pod):
    """
    Add compensation turning angle to the cp dictionary.

    With the distance to cp, and the current vector
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
    heading_offset = cp_info_dict['heading_offset']
    distance_to_cp = cp_info_dict['distance_to_cp']

    # how far the current heading will miss the target
    vector_overshoot = abs(
        distance_to_cp * math.tan(abs(heading_offset))
    )
    print(f"vector_overshoot {vector_overshoot}", file=sys.stderr)

    # the distance between pod and the overshoot point.
    extension_of_pod_vector_length = math.hypot(
        distance_to_cp, vector_overshoot
    )

    print(f"extension_of_pod_vector_length {extension_of_pod_vector_length}",
          file=sys.stderr)

    # coordinates of overshoot relative to pod

    x_of_vector_overshoot = (extension_of_pod_vector_length *
                             math.cos(pod['actual_heading_angle']))
    y_of_vector_overshoot = (extension_of_pod_vector_length *
                             math.sin(pod['actual_heading_angle']))

    # absolute values
    global_x_overshoot = (pod['x'] + x_of_vector_overshoot)
    global_y_overshoot = (pod['y'] - y_of_vector_overshoot)

    # distance between overshoot point and taget
    x_diff_overshoot_target = (global_x_overshoot - cp_info_dict['x'])
    y_diff_overshoot_target = (global_y_overshoot - cp_info_dict['y'])

    # compensation values (point opposite target from overshoot)
    cp_info_dict['x_compensation'] = int(-x_diff_overshoot_target)
    cp_info_dict['y_compensation'] = int(-y_diff_overshoot_target)


def get_corner_cut(next_cp, following_cp, pod):
    """
    Calculate where to aim to cut corner without missing target.

    Using the cp after the current target, calculate where
    in the next target, the pod should aim, so as to corner efficiently.
    Return an x and y coordinate.

    """

    x_between_next_and_following_cp = (
        next_cp['x'] - following_cp['x'])
    y_between_next_and_following_cp = (
        next_cp['y'] - following_cp['y'])

    distance_between_next_and_following_cp = math.hypot(
        x_between_next_and_following_cp,
        y_between_next_and_following_cp
    )

    # print(f"distance_between_target_and_following_cp",
    # "{distance_between_target_and_following_cp}", file=sys.stderr)

    x_between_pod_and_following_cp = following_cp['x'] - pod['x']
    y_between_pod_and_following_cp = following_cp['y'] - pod['y']

    distance_between_pod_and_following_cp = math.hypot(
        x_between_pod_and_following_cp,
        y_between_pod_and_following_cp)

    # print(f"distance_between_pod_and_following_cp",
    # f"{distance_between_pod_and_following_cp}", file=sys.stderr)

    # law of cosines
    angle_pod_next_following = math.acos(
        (
            distance_between_pod_and_following_cp ** 2 -
            next_cp['distance_to_cp'] ** 2 -
            distance_between_next_and_following_cp ** 2
        ) / (
            -2 * next_cp['distance_to_cp'] *
            distance_between_next_and_following_cp
        )
    )

    # +++++ NEXT TARGET COMP +++++

    # form a triangle between the pod, the target and the following cp
    # Then draw a line from the target towards the line formed between the pod
    # and the following cp. The line from the target should form a
    # right angle on the line from pod and following ckpoint.
    # The point where these lines meet, where the right angle is formed,
    # I will call 'c'

    angle_next_pod_following = math.asin(
        (distance_between_next_and_following_cp *
         math.sin(angle_pod_next_following)) /
        (distance_between_pod_and_following_cp)
    )

    distance_between_pod_and_c = (
        next_cp['distance_to_cp'] *
        math.cos(angle_next_pod_following)
    )

    coeff_distance_pod_c_and_pod_next = (
        distance_between_pod_and_c /
        distance_between_pod_and_following_cp
    )

    x_between_pod_and_c = (
        x_between_pod_and_following_cp *
        coeff_distance_pod_c_and_pod_next
    )
    y_between_pod_and_c = (
        y_between_pod_and_following_cp *
        coeff_distance_pod_c_and_pod_next
    )

    global_cx = pod['x'] + x_between_pod_and_c
    global_cy = pod['y'] + y_between_pod_and_c

    x_between_next_and_c = global_cx - next_cp['x']
    y_between_next_and_c = global_cy - next_cp['y']

    # print(f"x_between_next_and_c {x_between_next_and_c}",
    # file=sys.stderr)
    # print(f"y_between_next_and_c {y_between_next_and_c}",
    # file=sys.stderr)

    offset_from_next_center = 1100

    coeff_for_corner = (
        (offset_from_next_center ** 2) /
        (
            x_between_next_and_c ** 2 +
            y_between_next_and_c ** 2
        )
    )

    comp_x_next_c = x_between_next_and_c * coeff_for_corner
    comp_y_next_c = y_between_next_and_c * coeff_for_corner

    return {'x': comp_x_next_c, 'y': comp_y_next_c}

    # print(f"comp_x_target_c {comp_x_target_c}", file=sys.stderr)
    # print(f"comp_y_target_c {comp_y_target_c}", file=sys.stderr)


def get_info(pod):
    """Get info relating to pod."""
    # Establishing target cp
    pod['x'] = pod['x']
    pod_y = pod['y']
    global_vx = pod['global_vx']
    global_vy = pod['global_vy']
    angle_facing_in_rads = pod['angle_facing']
    next_cp_id = pod['next_cp_id']

    # translating global velocity as given to velocity relative to pod (0,0)
    pod['vx'] = pod_vx = global_vx
    pod['vy'] = pod_vy = global_vy * -1

    # getting the angle of the pods direction calculated from vector
    pod['actual_heading_angle'] = actual_heading_angle = (
        math.atan2(pod_vy, pod_vx)
    )  # TODO deal with zero values

    # getting the quadrant the vector is facing
    pod['vector_quad'] = vector_quad = quad_from_vector(pod_vx, pod_vy)

    # getting the absolute magnitude of pod vector
    pod['abs_velocity'] = abs_velocity = math.hypot(pod_vx, pod_vy)

    print(f" abs_velocity {int(abs_velocity)}", file=sys.stderr)

    next_cp = get_cp_info(next_cp_id, pod)

    facing_offset = (
        (
            (next_cp['abs_angle_to_cp'] -
             angle_facing_in_rads) + (pi / 2)
        ) % pi - (pi / 2)
    )
    heading_offset = (
        (
            (next_cp['abs_angle_to_cp'] -
             actual_heading_angle) + (pi / 2)
        ) % pi - (pi / 2)
    )

    add_compensation_angle_info(next_cp, pod)

    # ++++++++++++++++ANGLE TO NEXT cp+++++++++++++++++++++

    following_cp_id = (next_cp_id + 1) % (cp_count)
    # print(f"following cp id"
    #       f"{(next_cp_id + 1) % (cp_count)}",
    #       file=sys.stderr)

    following_cp = get_cp_info(following_cp_id, pod)

    corner_cut = get_corner_cut(next_cp, following_cp, pod)

    corner_cut_x = corner_cut['x']
    corner_cut_y = corner_cut['y']

    # +++++++++++++DISTANCE FROM PREVIOUS cp+++++++++++++++

    previous_cp_id = (next_cp_id - 1) % (cp_count)

    # print(f"previous_cp_id {previous_cp_id}",
    # file=sys.stderr)

    previous_cp_x = cps[previous_cp_id]['x']
    previous_cp_y = cps[previous_cp_id]['y']

    x_between_pod_and_previous_cp = pod['x'] - previous_cp_x
    y_between_pod_and_previous_cp = pod['y'] - previous_cp_y

    distance_between_pod_and_previous_cp = math.hypot(
        x_between_pod_and_previous_cp,
        y_between_pod_and_previous_cp)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++HEADING ALGORITHM+++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    heading_x = next_cp['x']
    heading_y = next_cp['y']

    thrust = 100

    if abs(facing_offset) > 1.5:
        thrust = 20
    elif abs(facing_offset) > 0.7:
        thrust = 90
    else:
        thrust = 100

    heading_x += int(corner_cut_x)
    heading_y += int(corner_cut_y)

    if abs(heading_offset) > 0.05:
        heading_x += int(next_cp['x_compensation'] * 0.3)
        heading_y += int(next_cp['y_compensation'] * 0.3)

    if abs_velocity > 0:
        time_to_target = (
            next_cp['distance_to_cp'] /
            abs_velocity
        )
        # print(f"time_to_target {time_to_target}", file=sys.stderr)

        if time_to_target < 5 and heading_offset < 0.9:
            thrust = 0
            # add_compensation_angle_info(following_cp, pod)
            heading_x = following_cp['x']
            heading_y = following_cp['y']

    pod['heading_x'] = heading_x
    pod['heading_y'] = heading_y
    pod['thrust'] = thrust


pod = {
    0: {},
    1: {},
    2: {},
    3: {}
}


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++GAME LOOP++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++


while True:
    counter += 1
    for i in range(2):

        x, y, global_vx, global_vy, angle_facing, next_cp_id = [
            int(j) for j in input().split()]

        # change to counter clockwise angle
        angle_facing = (-angle_facing) % 360
        # change to scale -180 0 180
        # (original angle seems to be off by 5 degrees,
        # hence the -175 instead of 180)
        angle_facing = (angle_facing - 175) % 360 - 180
        angle_facing_in_rads = angle_facing * (pi / 180)

        print(f" i:{i} next cp {next_cp_id} "
              f"angle facing:{angle_facing_in_rads} "
              f"x:{x}  y:{y} global_vx:{global_vx}  global_vy:{global_vy}",
              file=sys.stderr)

        pod[i]['x'] = x
        pod[i]['y'] = y
        pod[i]['global_vx'] = global_vx
        pod[i]['global_vy'] = global_vy
        pod[i]['angle_facing'] = angle_facing_in_rads
        pod[i]['next_cp_id'] = next_cp_id

        get_info(pod[i])
        print(f"{pod[i]}", file=sys.stderr)

    for i in range(2):
        # OPPONENT
        x_2, y_2, global_vx_2, global_vy_2, angle_2, next_check_point_id_2 = [
            int(j) for j in input().split()]

    print(f"{pod[0]['heading_x']} {pod[0]['heading_y']} {pod[0]['thrust']}")
    print(f"{pod[1]['heading_x']} {pod[1]['heading_y']} {pod[1]['thrust']}")
