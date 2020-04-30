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

    target_x = ckpnts[next_checkpoint_id]['x']
    target_y = ckpnts[next_checkpoint_id]['y']

    x_global_translation_to_target = target_x - pod_x
    y_global_translation_to_target = target_y - pod_y

    distance_to_target = math.hypot(
        x_global_translation_to_target,
        y_global_translation_to_target)

    pod_vx = global_vx
    pod_vy = global_vy * -1

    heading = math.atan2(pod_vy, pod_vx) # TODO deal with zero values
    vector_quad = quad_from_vector(pod_vx, pod_vy)

    abs_velocity = math.hypot(pod_vx, pod_vy)

    target_quadrant = quad_from_pos(target_x, target_y, pod_x, pod_y)

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

    abs_angle_to_target = abs_angle_to_target = math.atan2(
            y_to_target_from_pod, x_to_target_from_pod)

    facing_offset = ((abs_angle_to_target - angle_facing_in_rads) + (pi/2)) % pi - (pi/2)
    heading_offset = ((abs_angle_to_target - heading) + (pi/2)) % pi - (pi/2)

    return {
    #'x_global_translation_to_target':x_global_translation_to_target,
    #'y_global_translation_to_target':y_global_translation_to_target,
    'abs_angle_to_target':abs_angle_to_target,
    'target_x':target_x,
    'target_y':target_y,
    'pod_vx':pod_vx,
    'pod_vy':pod_vy,
    'x_to_target_from_pod':x_to_target_from_pod,
    'y_to_target_from_pod':y_to_target_from_pod,
    'distance_to_target':distance_to_target,
    'target_quadrant':target_quadrant,
    'vector_quad':vector_quad,
    'abs_velocity':abs_velocity,
    'heading':heading,
    'facing_offset':facing_offset,
    'heading_offset':heading_offset
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

        #for k in info.keys():
        #    print(f"{k}: {info[k]}", file=sys.stderr)
        
        thrust = 100
        thrustMultiplier = 1
        angleMultiplier = 1
  
        distToStartTurn = 1500
        distMultiplier = (info['distance_to_target'] / distToStartTurn) ** 3

        if info['distance_to_target'] > 6000 and abs(info['facing_offset']) < 0.1 and counter > 20:
            thrust = "BOOST"
        elif info['distance_to_target'] < distToStartTurn:
            thrustMultiplier = thrustMultiplier * distMultiplier
        
        #if isinstance(thrustMultiplier, complex):
        #    thrustMultiplier = 0.1

        if thrustMultiplier > 0.8:
            thrustMultiplier = 1
        if thrustMultiplier < 0.7:
            thrustMultiplier = 0.7
        
        if info['distance_to_target'] < 5000 or abs(info['facing_offset']) > 120:
            thrustMultiplier = thrustMultiplier * angleMultiplier
        
        if thrust != "BOOST":
            thrust = int(thrust * thrustMultiplier)
        
        if abs(info['heading_offset']) > 100 and abs(info['facing_offset']) > 90 and info['abs_velocity'] > 300:
            thrust = 0
        elif abs(info['heading_offset']) > 80 and abs(info['facing_offset']) > 40 and info['abs_velocity'] < 300:
            thrust = 80
        
        # HEADING
        
        #TODO REBUILD COMPLETELY!

        heading_x = ckpnts[next_checkpoint_id]['x']
        heading_y = ckpnts[next_checkpoint_id]['y']

        #get compensation for momentum
        '''
        print(f"""    distance to target :{info['distance_to_target']}
            global heading{info['heading']}
            ab angle to target{info['abs_angle_to_target']}
            target quadrant{info['target_quadrant']}
            heading {info['heading']}
            heading offset {info['heading_offset']}
            tan{math.tan(info['heading_offset'])}""", file=sys.stderr)
        '''
            

        if info['distance_to_target'] < 4000 and abs(info['heading_offset']) > 0.1 and abs(info['heading_offset']) < (pi/2):
            vector_overshoot = abs(info['distance_to_target'] * math.tan(info['heading_offset']))
            extension_of_pod_vector_length = math.hypot(info['distance_to_target'], vector_overshoot) # ERROR overshoot can become hypoteneuse!
            x_of_vector_overshoot = (extension_of_pod_vector_length * math.cos(info['heading'])) # relative to pod
            y_of_vector_overshoot = (extension_of_pod_vector_length * math.sin(info['heading'])) # relative to pod
            

            '''
            print(f"""      distance_to_target {info['distance_to_target']}
            vector_overshoot:{vector_overshoot}
            extension_of_pod_vector_length {extension_of_pod_vector_length}
            x_of_vector_overshoot {x_of_vector_overshoot}
            y_of_vector_overshoot {y_of_vector_overshoot}
            """, file=sys.stderr)
            '''

            abs_x_overshoot = x + x_of_vector_overshoot
            abs_y_overshoot = y + y_of_vector_overshoot

            x_diff_overshoot_target = abs_x_overshoot - ckpnts[next_checkpoint_id]['x'] 
            y_diff_overshoot_target = abs_y_overshoot - ckpnts[next_checkpoint_id]['y']

            x_compensation = int(ckpnts[next_checkpoint_id]['x'] + y_diff_overshoot_target)
            y_compensation = int(ckpnts[next_checkpoint_id]['y'] - x_diff_overshoot_target)

            heading_x = x_compensation
            heading_y = y_compensation

            print(f"""      distance_to_target {info['distance_to_target']}
            vector_overshoot:{vector_overshoot}
            extension_of_pod_vector_length {extension_of_pod_vector_length}
            x_of_vector_overshoot {x_of_vector_overshoot}
            y_of_vector_overshoot {y_of_vector_overshoot}
            x_diff_overshoot_target {x_diff_overshoot_target}
            y_diff_overshoot_target {y_diff_overshoot_target}
            """, file=sys.stderr)

        #print(f"{next_check_point_id}", file=sys.stderr, end="")

    #for i in range(2):
    for i in range(3):
        #OPPONENT
        x_2, y_2, global_vx_2, global_vy_2, angle_2, next_check_point_id_2 = [
            int(j) for j in input().split()]
     
    print(f"{heading_x} {heading_y} 100")
    #print(f"{pod[0]['target_x']} {pod[0]['target_y']} 100")
    print("5000 5000 0")
    #print(str(heading_x) + " " + str(heading_y) + " " + str(thrust))
    #print(str(heading_x2) + " " + str(heading_y2) + " " + str(thrust2))
