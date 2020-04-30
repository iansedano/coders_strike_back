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


def get_info(next_checkpoint_id, pod_x, pod_y, global_vx, global_vy, angle_facing_in_rads):

    # Establishing target checkpoint
    target_x = ckpnts[next_checkpoint_id]['x']
    target_y = ckpnts[next_checkpoint_id]['y']

    # x and y from pod to target
    x_global_translation_to_target = target_x - pod_x
    y_global_translation_to_target = target_y - pod_y

    # distance to target
    distance_to_target = math.hypot(
        x_global_translation_to_target,
        y_global_translation_to_target)

    print(f" distance_to_target {int(distance_to_target)}", file=sys.stderr)

    # translating global velocity as given to velocity relative to pod (0,0)
    pod_vx = global_vx
    pod_vy = global_vy * -1

    # getting the angle of the pods direction calculated from vector
    actual_heading_angle = math.atan2(pod_vy, pod_vx) # TODO deal with zero values

    # getting the quadrant the vector is facing
    vector_quad = quad_from_vector(pod_vx, pod_vy)

    # getting the absolute magnitude of pod vector
    abs_velocity = math.hypot(pod_vx, pod_vy)

    # getting the quadrant that the target is in relative to pod
    target_quadrant = quad_from_pos(target_x, target_y, pod_x, pod_y)

    # How far is the pod from the target in x and y
    x_to_target_from_pod = 0  # initalizing TODO deal with 0 values
    y_to_target_from_pod = 0  # initalizing TODO deal with 0 values

    if target_quadrant == 1:
        x_to_target_from_pod = target_x - pod_x
        y_to_target_from_pod = pod_y - target_y
    elif target_quadrant == 2:
        x_to_target_from_pod = (pod_x - target_x) * -1
        y_to_target_from_pod = pod_y - target_y
    elif target_quadrant == 3:
        x_to_target_from_pod = (pod_x - target_x) * -1
        y_to_target_from_pod = (target_y - pod_y) * -1
    elif target_quadrant == 4:
        x_to_target_from_pod = target_x - pod_x
        y_to_target_from_pod = (target_y - pod_y) * -1

    # getting the absolute angle of the target from the pods position
    abs_angle_to_target = abs_angle_to_target = math.atan2(
            y_to_target_from_pod, x_to_target_from_pod)

    #print(f" abs_angle_to_target {abs_angle_to_target}", file=sys.stderr)

    # the difference between the facing angle and the angle of the target
    # and the diff between the actual_heading_angle and the angle of the target
    # if 0 values, then pod is actual_heading_angle straight for the target
    facing_offset = ((abs_angle_to_target - angle_facing_in_rads) + (pi/2)) % pi - (pi/2)
    heading_offset = ((abs_angle_to_target - actual_heading_angle) + (pi/2)) % pi - (pi/2)

    #print(f" facing_offset {facing_offset}", file=sys.stderr)
    #print(f" heading_offset {heading_offset}", file=sys.stderr)


    heading_x = target_x
    heading_y = target_y

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # ++++++++++++++++++++COMPENSATION ANGLE+++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


    if abs(heading_offset) > 0.05:
        # how far the current heading will miss the target
        vector_overshoot = abs(distance_to_target * math.tan(abs(heading_offset)))
        #print(f" vector overshoot {int(vector_overshoot)}", file=sys.stderr)

        # the distance between pod and the line crossing of the target
        extension_of_pod_vector_length = math.hypot(distance_to_target, vector_overshoot)
        #print(f" extension_of_pod_vector_length {int(extension_of_pod_vector_length)}", file=sys.stderr)

        # coordinates of the overshoot
        x_of_vector_overshoot = (extension_of_pod_vector_length * math.cos(actual_heading_angle)) # relative to pod
        y_of_vector_overshoot = (extension_of_pod_vector_length * math.sin(actual_heading_angle)) # relative to pod
        
        #print(f" x_of_vector_overshoot {int(x_of_vector_overshoot)}", file=sys.stderr)
        #print(f" y_of_vector_overshoot {int(y_of_vector_overshoot)}", file=sys.stderr)

        #absolute values
        abs_x_overshoot = pod_x + x_of_vector_overshoot
        abs_y_overshoot = pod_y - y_of_vector_overshoot

        #print(f" abs_x_overshoot {int(abs_x_overshoot)}", file=sys.stderr)
        #print(f" abs_y_overshoot {int(abs_y_overshoot)}", file=sys.stderr)

        # distance between overshoot point and taget
        x_diff_overshoot_target = abs_x_overshoot - target_x
        y_diff_overshoot_target = abs_y_overshoot - target_y

        #print(f" x_diff_overshoot_target {int(x_diff_overshoot_target)}", file=sys.stderr)
        # print(f" y_diff_overshoot_target {int(y_diff_overshoot_target)}", file=sys.stderr)

        x_compensation = int(target_x - x_diff_overshoot_target)
        y_compensation = int(target_y - y_diff_overshoot_target)

        #print(f" x_compensation {int(x_compensation)}", file=sys.stderr)
        #print(f" y_compensation {int(y_compensation)}", file=sys.stderr)

        heading_x = x_compensation
        heading_y = y_compensation

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++ANGLE TO NEXT CHECKPOINT++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


    following_checkpoint_x = ckpnts[(next_checkpoint_id + 1) % (checkpoint_count)]['x']
    following_checkpoint_y = ckpnts[(next_checkpoint_id + 1) % (checkpoint_count)]['y']

    print(f"following checkpoint id {(next_checkpoint_id + 1) % (checkpoint_count)}", file=sys.stderr)

    x_between_target_and_following_checkpoint = target_x - following_checkpoint_x
    y_between_target_and_following_checkpoint = target_y - following_checkpoint_y

    distance_between_target_and_following_checkpoint = math.hypot(x_between_target_and_following_checkpoint,y_between_target_and_following_checkpoint)

    print(f"distance_between_target_and_following_checkpoint {distance_between_target_and_following_checkpoint}", file=sys.stderr)

    x_between_pod_and_following_checkpoint = pod_x - following_checkpoint_x
    y_between_pod_and_following_checkpoint = pod_y - following_checkpoint_y

    distance_between_pod_and_following_checkpoint = math.hypot(x_between_pod_and_following_checkpoint, y_between_pod_and_following_checkpoint)

    print(f"distance_between_pod_and_following_checkpoint {distance_between_pod_and_following_checkpoint}", file=sys.stderr)
    # law of cosines
    angle_between_pod_and_following_checkpoint = math.acos(
            (
                distance_between_pod_and_following_checkpoint ** 2 -
                distance_to_target ** 2 -
                distance_between_target_and_following_checkpoint **2
            ) / (
                -2 * distance_to_target * distance_between_target_and_following_checkpoint
            )
        )

    print(f"angle_between_pod_and_following_checkpoint {angle_between_pod_and_following_checkpoint}", file=sys.stderr)


    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++FACING ANGLE MANAGEMENT+++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    print(f" facing offset {facing_offset}", file=sys.stderr)

    thrust = 100
    if abs(facing_offset) > 1.5:
        thrust = 20
    elif abs(facing_offset) > 0.7:
        thrust = 50
    else:
        thrust = 100

    if distance_to_target < 1000:
        thrust = 10



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
    0:{'info':{}, },
    1:{'info':{}, },
    2:{'info':{}, },
    3:{'info':{}, }
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

        info = get_info(next_checkpoint_id, x, y, global_vx, global_vy, angle_facing_in_rads)


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
