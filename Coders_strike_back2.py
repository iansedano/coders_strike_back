import sys
import math
import numpy as np

laps = int(input())
checkpoint_count = int(input())

ckpnts = {}
for i in range(checkpoint_count):
    checkpoint_x, checkpoint_y = [int(j) for j in input().split()]
#    print(f"{checkpoint_x}", file=sys.stderr)
    ckpnts[i] = {'x': checkpoint_x, 'y': checkpoint_y}
checkpoint_count
print(f"checkpoint count {checkpoint_count}", file=sys.stderr)
# print(f"test {ckpnts[1]['x']}", file=sys.stderr)

counter = 0

def pp_angle(a):
    new_a = a
    if a < 0:
        new_a = a + 360
    return new_a

pi = 3.14159

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def quad_from_pos(target_x, target_y, x, y):  # target x
    if target_x > x and target_y < y:
        return 1
    elif target_x < x and target_y < y:
        return 2
    elif target_x < x and target_y > y:
        return 3
    elif target_x > x and target_y > y:
        return 4


def quad_from_vector(global_vx, global_vy):
    if global_vx > 0 and global_vy > 0:
        return 1
    elif global_vx < 0 and global_vy > 0:
        return 2
    elif global_vx < 0 and global_vy < 0:
        return 3
    elif global_vx > 0 and global_vy < 0:
        return 4

def get_checkpoint_info(checkpoint_id, pod):
    pod['x'] = pod_x
    pod['y'] = pod_y

    x = ckpnts[checkpoint_id]['x']
    y = ckpnts[checkpoint_id]['y']

    # x and y from pod to checkpoint
    pod_to_checkpoint_x = x - pod_x
    pod_to_checkpoint_y = y - pod_y

    # distance to checkpoint
    distance_to_checkpoint = math.hypot(
        pod_to_checkpoint_x,
        pod_to_checkpoint_y)

    print(f" distance_to_checkpoint {int(distance_to_checkpoint)}", file=sys.stderr)

    checkpoint_quadrant = quad_from_pos(x, y, pod_x, pod_y)

    x_to_checkpoint_from_pod = 0  # initalizing TODO deal with 0 values
    y_to_checkpoint_from_pod = 0  # initalizing TODO deal with 0 values

    if checkpoint_quadrant == 1:
        x_to_checkpoint_from_pod = x - pod_x
        y_to_checkpoint_from_pod = pod_y - y
    elif checkpoint_quadrant == 2:
        x_to_checkpoint_from_pod = (pod_x - x) * -1
        y_to_checkpoint_from_pod = pod_y - y
    elif checkpoint_quadrant == 3:
        x_to_checkpoint_from_pod = (pod_x - x) * -1
        y_to_checkpoint_from_pod = (y - pod_y) * -1
    elif checkpoint_quadrant == 4:
        x_to_checkpoint_from_pod = x - pod_x
        y_to_checkpoint_from_pod = (y - pod_y) * -1


    # getting the absolute angle of the checkpoint from the pods position
    abs_angle_to_checkpoint = abs_angle_to_checkpoint = math.atan2(
        y_to_checkpoint_from_pod, x_to_checkpoint_from_pod)

    return{
    'x':x,
    'y':y,
    'pod_to_checkpoint_x':pod_to_checkpoint_x,
    'pod_to_checkpoint_y':pod_to_checkpoint_y,
    'distance_to_checkpoint':distance_to_checkpoint,
    'checkpoint_quadrant': checkpoint_quadrant,
    'x_to_checkpoint_from_pod': x_to_checkpoint_from_pod,
    'y_to_checkpoint_from_pod': y_to_checkpoint_from_pod,
    'abs_angle_to_checkpoint': abs_angle_to_checkpoint,
    }


def get_info(pod):

    # Establishing target checkpoint
    pod_x = pod['x']
    pod_y = pod['y']
    global_vx = pod['global_vx']
    global_vy = pod['global_vy']
    angle_facing_in_rads = pod['angle_facing']
    next_checkpoint_id = pod['next_checkpoint_id']

    next_checkpoint = get_checkpoint_info(next_checkpoint_id, pod)

    # translating global velocity as given to velocity relative to pod (0,0)
    pod_vx = global_vx
    pod_vy = global_vy * -1

    # getting the angle of the pods direction calculated from vector
    actual_heading_angle = math.atan2(pod_vy, pod_vx) # TODO deal with zero values

    # getting the quadrant the vector is facing
    vector_quad = quad_from_vector(pod_vx, pod_vy)

    # getting the absolute magnitude of pod vector
    abs_velocity = math.hypot(pod_vx, pod_vy)
    print(f" abs_velocity {int(abs_velocity)}", file=sys.stderr)

    facing_offset = ((abs_angle_to_target - angle_facing_in_rads) + (pi/2)) % pi - (pi/2)
    heading_offset = ((abs_angle_to_target - actual_heading_angle) + (pi/2)) % pi - (pi/2)

    #print(f" facing_offset {facing_offset}", file=sys.stderr)
    #print(f" heading_offset {heading_offset}", file=sys.stderr)


    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++COMPENSATION ANGLE+++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    

    # how far the current heading will miss the target
    vector_overshoot = abs(distance_to_target * math.tan(abs(heading_offset)))

    # the distance between pod and the line crossing of the target
    extension_of_pod_vector_length = math.hypot(distance_to_target, vector_overshoot)

    # coordinates of the overshoot
    x_of_vector_overshoot = (extension_of_pod_vector_length * math.cos(actual_heading_angle)) # relative to pod
    y_of_vector_overshoot = (extension_of_pod_vector_length * math.sin(actual_heading_angle)) # relative to pod
    

    #absolute values (constrained to max 2000)
    global_x_overshoot = (pod_x + x_of_vector_overshoot)
    global_y_overshoot = (pod_y - y_of_vector_overshoot)

    # distance between overshoot point and taget
    x_diff_overshoot_target = global_x_overshoot - target_x
    y_diff_overshoot_target = global_y_overshoot - target_y

    # compensation values
    x_compensation = int(0 - x_diff_overshoot_target)
    y_compensation = int(0 - y_diff_overshoot_target)


    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++CHECKPOINT TRACKING++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   

    
    # ++++++++++++++++ANGLE TO NEXT CHECKPOINT+++++++++++++++++++++

    following_checkpoint_id = (next_checkpoint_id + 1) % (checkpoint_count)
    # print(f"following checkpoint id {(next_checkpoint_id + 1) % (checkpoint_count)}", file=sys.stderr)

    following_checkpoint_x = ckpnts[following_checkpoint_id]['x']
    following_checkpoint_y = ckpnts[following_checkpoint_id]['y']

    x_between_target_and_following_checkpoint = target_x - following_checkpoint_x
    y_between_target_and_following_checkpoint = target_y - following_checkpoint_y

    distance_between_target_and_following_checkpoint = math.hypot(x_between_target_and_following_checkpoint,y_between_target_and_following_checkpoint)

    # print(f"distance_between_target_and_following_checkpoint {distance_between_target_and_following_checkpoint}", file=sys.stderr)

    x_between_pod_and_following_checkpoint = following_checkpoint_x - pod_x
    y_between_pod_and_following_checkpoint = following_checkpoint_y - pod_y

    distance_between_pod_and_following_checkpoint = math.hypot(x_between_pod_and_following_checkpoint, y_between_pod_and_following_checkpoint)

    # print(f"distance_between_pod_and_following_checkpoint {distance_between_pod_and_following_checkpoint}", file=sys.stderr)
    # law of cosines
    angle_pod_target_following_checkpoint = math.acos(
            (
                distance_between_pod_and_following_checkpoint ** 2 -
                distance_to_target ** 2 -
                distance_between_target_and_following_checkpoint **2
            ) / (
                -2 * distance_to_target * distance_between_target_and_following_checkpoint
            )
        )


    # +++++ NEXT TARGET COMP +++++

    # form a triangle between the pod, the target and the following checkpoint
    # Then draw a line from the target towards the line formed between the pod and the following checkpoint
    # The line from the target should form a right angle on the line from pod and following ckpoint.
    # The point where these lines meet, where the right angle is formed, I will call 'c'

    angle_target_pod_following = math.asin(
        (distance_between_target_and_following_checkpoint * math.sin(angle_pod_target_following_checkpoint) )
        /
        (distance_between_pod_and_following_checkpoint)
        )

    distance_between_pod_and_c = distance_to_target * math.cos(angle_target_pod_following)

    coeff_distance_pod_c_and_pod_target = distance_between_pod_and_c / distance_between_pod_and_following_checkpoint

    x_between_pod_and_c = x_between_pod_and_following_checkpoint * coeff_distance_pod_c_and_pod_target
    y_between_pod_and_c = y_between_pod_and_following_checkpoint * coeff_distance_pod_c_and_pod_target

    global_cx = pod_x + x_between_pod_and_c
    global_cy = pod_y + y_between_pod_and_c

    x_between_target_and_c = global_cx - target_x
    y_between_target_and_c = global_cy - target_y

    print(f"x_between_target_and_c {x_between_target_and_c}", file=sys.stderr)
    print(f"y_between_target_and_c {y_between_target_and_c}", file=sys.stderr)

    offset_from_target_center = 1100

    coeff_for_corner = (offset_from_target_center ** 2) / (x_between_target_and_c ** 2 + y_between_target_and_c ** 2)

    comp_x_target_c = x_between_target_and_c * coeff_for_corner
    comp_y_target_c = y_between_target_and_c * coeff_for_corner

    print(f"comp_x_target_c {comp_x_target_c}", file=sys.stderr)
    print(f"comp_y_target_c {comp_y_target_c}", file=sys.stderr)



    # print(f"angle_pod_target_following_checkpoint {angle_pod_target_following_checkpoint}", file=sys.stderr)


    # +++++++++++++DISTANCE FROM PREVIOUS CHECKPOINT+++++++++++++++

    previous_checkpoint_id = (next_checkpoint_id - 1) % (checkpoint_count)

    print(f"previous_checkpoint_id {previous_checkpoint_id}", file=sys.stderr)

    previous_checkpoint_x = ckpnts[previous_checkpoint_id]['x']
    previous_checkpoint_y = ckpnts[previous_checkpoint_id]['y']

    x_between_pod_and_previous_checkpoint = pod_x - previous_checkpoint_x
    y_between_pod_and_previous_checkpoint = pod_y - previous_checkpoint_y

    distance_between_pod_and_previous_checkpoint = math.hypot(x_between_pod_and_previous_checkpoint, y_between_pod_and_previous_checkpoint)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++HEADING ALGORITHM+++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    heading_x = target_x
    heading_y = target_y


    thrust = 100

    if abs(facing_offset) > 1.5:
        thrust = 20
    elif abs(facing_offset) > 0.7:
        thrust = 90
    else:
        thrust = 100


    heading_x += int(comp_x_target_c)
    heading_y += int(comp_y_target_c)

    if abs(heading_offset) > 0.05:
        heading_x += x_compensation
        heading_y += y_compensation

    if abs_velocity > 0:
        time_to_target = distance_to_target / abs_velocity
        print(f"time_to_target {time_to_target}", file=sys.stderr)

        if time_to_target < 5 and heading_offset < 0.1:
            thrust = 20
            heading_x = following_checkpoint_x
            heading_y = following_checkpoint_y



    return {
    #'x_global_translation_to_target':x_global_translation_to_target,
    #'y_global_translation_to_target':y_global_translation_to_target,
    # 'abs_angle_to_target':abs_angle_to_target,
    # 'target_x':target_x,
    # 'target_y':target_y,
    # 'pod_vx':pod_vx,
    # 'pod_vy':pod_vy,
    # 'x_to_target_from_pod':x_to_target_from_pod,
    # 'y_to_target_from_pod':y_to_target_from_pod,
     'distance_to_target':distance_to_target,
    # 'target_quadrant':target_quadrant,
    # 'vector_quad':vector_quad,
    # 'abs_velocity':abs_velocity,
    # 'actual_heading_angle':actual_heading_angle,
     'facing_offset':facing_offset,
    # 'heading_offset':heading_offset,
    # 'vector_overshoot':vector_overshoot,
    # 'extension_of_pod_vector_length':extension_of_pod_vector_length,
    # 'x_of_vector_overshoot':x_of_vector_overshoot,
    # 'y_of_vector_overshoot':y_of_vector_overshoot,
    # 'x_diff_overshoot_target':x_diff_overshoot_target,
    # 'y_diff_overshoot_target':y_diff_overshoot_target,
    # 'x_compensation':x_compensation,
    # 'y_compensation':y_compensation,
    'heading_x':heading_x,
    'heading_y':heading_y,
    'thrust':thrust
    }


pod = {
    0:{},
    1:{},
    2:{},
    3:{}
    }
# game loop
while True:
    counter += 1
    #for i in range(2):
    for i in range(1):

        x, y, global_vx, global_vy, angle_facing, next_checkpoint_id = [
            int(j) for j in input().split()]

        angle_facing = (-angle_facing) % 360 # changing to counter clockwise angle
        angle_facing = (angle_facing - 175) % 360 - 180 # changing to scale -180 0 180 (original angle seems to be off by 5 degrees, hence the -175 instead of 180)
        angle_facing_in_rads = angle_facing * (pi / 180) 
        print(f" i:{i} next checkpoint {next_checkpoint_id} angle facing:{angle_facing_in_rads},  x:{x}  y:{y} global_vx:{global_vx}  global_vy:{global_vy}", file=sys.stderr)

        pod[i]['x'] = x
        pod[i]['y'] = y
        pod[i]['global_vx'] = global_vx
        pod[i]['global_vy'] = global_vy
        pod[i]['angle_facing'] = angle_facing_in_rads
        pod[i]['next_checkpoint_id'] = next_checkpoint_id

        pod[i]['info'] = get_info(pod[i])


    #for i in range(2):
    for i in range(3):
        #OPPONENT
        x_2, y_2, global_vx_2, global_vy_2, angle_2, next_check_point_id_2 = [
            int(j) for j in input().split()]
     
    print(f"{info['heading_x']} {info['heading_y']} {info['thrust']}")
    #print(f"{pod[0]['target_x']} {pod[0]['target_y']} 100")
    print("5000 5000 0")
    #print(str(heading_x) + " " + str(heading_y) + " " + str(thrust))
    #print(str(heading_x2) + " " + str(heading_y2) + " " + str(thrust2))
