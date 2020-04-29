import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

#next_checkpoint_tracker = next_checkpoint_dist

# while next_checkpoint_dist == next_checkpoint_dist

# game loop

counter = 0

lastx = 0
lasty = 0
dx = 0
dy = 0

checkpoints = []


def pp_angle(a):
    new_a = a
    if a < 0:
        new_a = a + 360
    return new_a


while True:
    counter += 1

    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [
        int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]

    if counter > 1:
        dx = x - lastx
        dy = y - lasty
    lastx = x
    lasty = y

    vector_mag = (dx**2 + dy**2)**0.5
    # N: -90  S: 90  W: 180 / -180 E: 0
    vector_heading = math.atan2(dy, dx) / math.pi * 180
    vector_heading = pp_angle(vector_heading)

    x_ship_to_target = next_checkpoint_x - x
    y_ship_to_target = next_checkpoint_y - y

    angle_to_target = math.atan2(
        y_ship_to_target, x_ship_to_target) / math.pi * 180
    angle_to_target = pp_angle(angle_to_target)

    angle_diff = 0
    angle_diff = angle_to_target - vector_heading
    angle_diff = (angle_diff + 180) % 360 - 180

    # predicting next position

    next_x = x + dx
    next_y = y + dy

    # THRUSTING

    thrust = 100
    thrustMultiplier = 1

    # angle multi
    angleMultiplier = 1

    if abs(next_checkpoint_angle) > 90:
        angleMultiplier = 0
    elif abs(next_checkpoint_angle) <= 90 and abs(next_checkpoint_angle) >= 40:
        angleMultiplier = (abs(next_checkpoint_angle) - 90) / -50
    elif abs(next_checkpoint_angle) < 50:
        angleMultiplier = 1

    # distance multi

    distToStartTurn = 1500
    distMultiplier = (next_checkpoint_dist / distToStartTurn) ** 3

    if next_checkpoint_dist > 6000 and abs(next_checkpoint_angle) < 5 and counter > 20:
        thrust = "BOOST"

    elif next_checkpoint_dist < distToStartTurn:
        thrustMultiplier = thrustMultiplier * distMultiplier

   # if isinstance(thrustMultiplier, complex):
   #     thrustMultiplier = 0.1

    if thrustMultiplier > 0.8:
        thrustMultiplier = 1
    if thrustMultiplier < 0.7:
        thrustMultiplier = 0.7

    if next_checkpoint_dist < 5000 or abs(next_checkpoint_angle) > 120:
        thrustMultiplier = thrustMultiplier * angleMultiplier

    if thrust != "BOOST":
        thrust = int(thrust * thrustMultiplier)

    if abs(angle_diff) > 100 and abs(next_checkpoint_angle) > 90 and abs(vector_mag) > 300:
        thrust = 0
    elif abs(angle_diff) > 80 and abs(next_checkpoint_angle) > 40 and abs(vector_mag) < 300:
        thrust = 80

    # HEADING

    heading_x = next_checkpoint_x
    heading_y = next_checkpoint_y

    comp_vector_angle = 0  # compensating vector
    comp_x = -y_ship_to_target
    comp_y = -x_ship_to_target

    # /math.pi*180 # N: -90  S: 90  W: 180 / -180 E: 0
    comp_angle = math.atan2(comp_y, comp_x)
    #comp_angle = pp_angle(comp_angle)

    comp_x = 400 * math.cos(comp_angle)
    comp_y = 400 * math.sin(comp_angle)

    if dy > 0:  # going down
        if angle_diff > 1:
            heading_x += int(comp_x)
            heading_y -= int(comp_y)
        elif angle_diff < -1:
            heading_x -= int(comp_x)
            heading_y += int(comp_y)
    elif dy < 0:  # going up
        if angle_diff > 1:
            heading_x += int(comp_x)
            heading_y -= int(comp_y)
        elif angle_diff < -1:
            heading_x -= int(comp_x)
            heading_y += int(comp_y)

    # math.degrees(x)
    # Convert angle x from radians to degrees.

    # math.radians(x)
    # Convert angle x from degrees to radians.

    #angle_diff = (angle_diff + 180) % 360 - 180

    # DEBUGGING
    print("dx ", file=sys.stderr, end="")
    print(dx, file=sys.stderr)
    print("dy ", file=sys.stderr, end="")
    print(dy, file=sys.stderr)
    print("comp x ", file=sys.stderr, end="")
    print(comp_x, file=sys.stderr)
    print("comp y ", file=sys.stderr, end="")
    print(comp_y, file=sys.stderr)
    print("comp_angle ", file=sys.stderr, end="")
    print(comp_angle, file=sys.stderr)
    print("angle diff ", file=sys.stderr, end="")
    print(angle_diff, file=sys.stderr)
    #print("angle to target ", file=sys.stderr, end = "")
    #print(angle_to_target, file=sys.stderr)
    print("vector_mag ", file=sys.stderr, end="")
    print(vector_mag, file=sys.stderr)
    print("vector_heading ", file=sys.stderr, end="")
    print(vector_heading, file=sys.stderr)
    #print("distMultiplier ", file=sys.stderr, end = "")
    #print(distMultiplier, file=sys.stderr)
    #print("angleMultiplier ", file=sys.stderr, end = "")
    #print(angleMultiplier, file=sys.stderr)
    #print("thrustMultiplier ", file=sys.stderr, end = "")
    #print(thrustMultiplier, file=sys.stderr)
    print("thrust " + str(thrust), file=sys.stderr)
    #print("distance " + str(next_checkpoint_dist), file=sys.stderr)
    print("next_checkpoint_angle " + str(next_checkpoint_angle), file=sys.stderr)

    # You have to output the target position
    # followed by the power (0 <= thrust <= 100)
    # i.e.: "x y thrust"

    # if abs(opponent_x - x) < 1000 and abs(opponent_y - y) < 1000 and counter > 30:
    #    print(str(opponent_x) + " " + str(opponent_y) + " " + str(100))
    # else :
    print(str(heading_x) + " " + str(heading_y) + " " + str(thrust))
