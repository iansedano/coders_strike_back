"""
Coders Strike back Gold League Bot.

Currently standing in at around 100th in Gold league.

All angles in radians where possible in scale of pi to -pi

cp = cp
rel = relation
agl = angle
d = d


"""
import sys
import math

# for vector math refernce.
# https://www.oreilly.com/library/view/machine-learning-with/9781491989371/ch01.html

pi = 3.14159




# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++POINT & VECTOR+++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return point(x, y)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return point(x, y)

    def __mul__(self, num):
        x = self.x * num
        y = self.y * num
        return point(x, y)

    def flip(self):
        """ Flip around axis
        Only to be used when pod is taken as (0,0)"""
        x = self.x * -1
        y = self.y * -1
        return point(x, y)


class vector:
    def __init__(self, vx, vy):
        self.x = vx
        self.y = vy
        self.angle = math.atan2(self.y, self.x)
        self.abs = math.hypot(self.x, self.y)

    def get_quadrant(self):
        """Get the quadrant a vector is facing."""
        if self.x > 0 and self.y > 0:
            self.quadrant = 1
        elif self.x < 0 and self.y > 0:
            self.quadrant = 2
        elif self.x < 0 and self.y < 0:
            self.quadrant = 3
        elif self.x > 0 and self.y < 0:
            self.quadrant = 4

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++CHECKPOINT+++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class cp:  # Checkpoint
    def __init__(self, pos, id):
        self.pos = pos
        self.id = id

class rel:
    def __init__(self, pod, cp):
        self.d = get_distance(pod.pos, cp.pos)
        self.parent_cp = cp
        translation_pod_cp = get_relative_pos_from_global(pod.pos, cp.pos)
        self.abs_angle = translation_pod_cp.angle
        self.facing_offset = get_signed_angle(
                                self.abs_angle, pod.angle_facing)
        self.heading_offset = get_signed_angle(
                                self.abs_angle, pod.vector.angle)

    def add_compensation_angle(self, pod, limit=7000):

        global_overshoot = get_overshoot_pos(
            self, pod, pod.vector.angle, pod.current_cp_rel.heading_offset)

        # compensation values (point opposite target from overshoot)

        self.compensation = constrain_point(global_overshoot.flip(), -limit, limit)

    def compensated_heading(self):

        return self.parent_cp.pos + self.compensation

class heading:
    def __init__(self, pod):
        self.pod

class compensation:
    def __init__(vector, target)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++POD+++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class pod:
    def __init__(self, pos, global_vector, angle_facing, current_cp):
        self.pos = pos
        self.global_vector = global_vector
        self.angle_facing = angle_facing
        self.current_cp = current_cp
        self.next_cp = cps[(current_cp.id + 1) % (cp_count)]
        self.last_cp = cps[(current_cp.id - 1) % (cp_count)]
        self.next_cp2 = cps[(current_cp.id + 2) % (cp_count)]
        self.vector = vector(self.global_vector.x, self.global_vector.y * -1)
        self.current_cp_rel = rel(self, self.current_cp)
        self.next_cp_rel = rel(self, self.next_cp)

    def get_heading(self):

        # Set a base heading in case none of the if statements catch
        self.current_cp_rel.add_compensation_angle(self, limit=5000)
        base_heading = self.current_cp_rel.compensated_heading()
        self.heading = base_heading
        self.thrust = 100

        # +++++++ HEADING ALGORITHM +++++
        
        # If far enough, boost
        if (
                self.current_cp_rel.d > 6000 and
                abs(self.current_cp_rel.facing_offset) < 0.1):
            self.thrust = "BOOST"

        # +++ Getting info about the corner to take+++
        self.angle_pod_current_next = get_angle_between_three_points(
                                        self.pos,
                                        self.current_cp.pos,
                                        self.next_cp.pos)
        d_last_cp_current_cp = get_distance(
                                        self.last_cp.pos,
                                        self.current_cp.pos)
        d_pod_last_cp = get_distance(
                                        self.pos,
                                        self.last_cp.pos)

        # if far enough, and heading in the right direction
        # swing out in preparation for the corner.
        if (
                # d_pod_last_cp > 1000 and
                self.current_cp_rel.d > d_pod_last_cp * 3 and
                self.current_cp_rel.heading_offset < pi/4 and
                d_last_cp_current_cp > 5000):
            debug("status - prepping corner")
            self.heading = self.prepare_corner()

        # if heading is good, activate corner procedure
        if (
                self.vector.abs > 0 and
                abs(self.current_cp_rel.heading_offset) < 0.7):
            debug("status - cornering")
            self.corner()

        # if facing the wrong direction, do not thrust...
        # facing_compensation(self)

    def prepare_corner(self, limit=5000):

        direction = left_or_right(
                        self.pos,
                        self.current_cp.pos,
                        self.next_cp.pos)

        mag = pi/10 # magnitude of compensation move

        if direction == "left":
            sim_heading = self.current_cp_rel.abs_angle - mag
        elif direction == "right":
            sim_heading = self.current_cp_rel.abs_angle + mag

        prep_heading = get_overshoot_pos(
            self.current_cp_rel, self, sim_heading, mag)

        prep_heading = constrain_point(prep_heading, -limit, limit)

        new_heading = self.current_cp.pos + prep_heading

        return new_heading

    def corner(self):

        time_to_target = (self.current_cp_rel.d / self.vector.abs)

        self.next_cp_rel.add_compensation_angle(self, limit=5000)

        #next_heading = self.next_cp_rel.compensated_heading()
        next_heading = self.next_cp.pos

        debug(self.current_cp_rel.heading_offset)

        if abs(self.angle_pod_current_next) > pi * 4/5:
            print(f"full speed", file=sys.stderr)
            if time_to_target < 5.5:
                self.heading = next_heading
                self.thrust = "BOOST"

        elif abs(self.angle_pod_current_next) > pi * 3/5:
            print(f"soft", file=sys.stderr)
            if time_to_target < 5.5:
                self.heading = next_heading
                self.thrust = 100

        elif abs(self.angle_pod_current_next) > pi * 2/5:
            print(f"90", file=sys.stderr)
            if time_to_target < 4.5:
                self.heading = next_heading
                self.thrust = 100
            elif time_to_target < 5.5:
                self.heading = next_heading
                self.thrust = 10

        elif abs(self.angle_pod_current_next) > pi * 1/5:
            print(f"hard", file=sys.stderr)
            if time_to_target < 3.05:
                self.heading = next_heading
                self.thrust = 100
            elif time_to_target < 5.5:
                self.heading = next_heading
                self.thrust = 20

        elif abs(self.angle_pod_current_next) < pi * 1/5:
            print(f"hairpin", file=sys.stderr)
            if time_to_target < 5:
                self.heading = next_heading
                self.thrust = 0

    def predict_next_pos(self):

        new_x = self.pos.x + self.global_vector.x
        new_y = self.pos.y + self.global_vector.y

        self.next_pos = point(new_x, new_y)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++ANGLE FUNCTIONS+++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def flip_rotation_direction(angle, type="radians"):
    if type == "degrees":
        angle = (-angle) % 360
    elif type == "radians":
        angle = (-angle) % pi
    return angle

def change_angle_scale_to_180(angle):
    angle = (angle - 180) % 360 - 180
    return angle

def degree_to_rads(angle):
    angle = angle * (pi / 180)
    return angle

def find_quadrant(origin, target):
    """Get the target quadrant from an x and y position."""
    if target.x > origin.x and target.y < origin.y:
        return 1
    elif target.x < origin.x and target.y < origin.y:
        return 2
    elif target.x < origin.x and target.y > origin.y:
        return 3
    elif target.x > origin.x and target.y > origin.y:
        return 4

def get_signed_angle(a1, a2):

    diff = a1 - a2
    if diff > pi:
        diff -= pi*2
    if diff < -pi:
        diff += pi*2

    return diff

def facing_compensation(pod):

    if abs(pod.current_cp_rel.facing_offset) > pi * 4/5:
        pod.thrust = 20

    elif abs(pod.current_cp_rel.facing_offset) > pi * 3/5:
        pod.thrust = 30

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++UTILITY FUNCTIONS+++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def debug(var_name="", variable=""):
    print(f"{var_name}, {variable}", file=sys.stderr)

def constrain(val, min_val, max_val):
    """Constrain value between min and max."""
    val = int(min(max_val, max(min_val, val)))

    return val

def constrain_point(pos, min_val, max_val):
    """ Constrain the magnitude from (0,0) of a point

        Generally used to limit the compensation of a heading."""

    x = int(constrain(pos.x, min_val, max_val))
    y = int(constrain(pos.y, min_val, max_val))

    return point(x, y)

def get_distance(point1, point2):
    """ Get distance between two points """

    x = point2.x - point1.x
    y = point2.y - point1.y
    d = math.hypot(x, y)
    return d

def get_relative_pos_from_global(p1, p2):
    """ Get vector from two positions """

    quadrant = find_quadrant(p1, p2)

    x = 0
    y = 0

    if quadrant == 1:
        x = p2.x - p1.x
        y = p1.y - p2.y
    elif quadrant == 2:
        x = (p1.x - p2.x) * -1
        y = p1.y - p2.y
    elif quadrant == 3:
        x = (p1.x - p2.x) * -1
        y = (p2.y - p1.y) * -1
    elif quadrant == 4:
        x = p2.x - p1.x
        y = (p2.y - p1.y) * -1

    return vector(x, y)

def get_global_angle(p1, p2):
    """
        Get global angle between two points

        That is, if a p1 is the pod, at (0, 0)
        and p2 is at (-100, 100)
        The global angle would be 3/4 pi
        """
    d = get_distance(p1, p2)
    q = find_quadrant(p1, p2)

    diff = p1 - p2

    local_angle = math.atan2(diff.y, diff.x)

    global_angle = 0

    if q == 1:
        global_angle = pi - local_angle
    elif q == 2:
        global_angle = pi - local_angle
    elif q == 3:
        global_angle = -pi - local_angle
    elif q == 4:
        global_angle = -pi - local_angle

    return global_angle

def get_angle_between_three_points(p1, p2, p3):
    """ Get angle between three points

        At p2 between p1 and p3 """

    d_p1_p2 = get_distance(p1, p2)
    d_p2_p3 = get_distance(p2, p3)
    d_p1_p3 = get_distance(p1, p3)

    # law of cosines
    angle = (
        math.acos(
                    (
                        d_p1_p3 ** 2 - d_p1_p2 ** 2 - d_p2_p3 ** 2
                    ) / (
                        -2 * d_p1_p2 * d_p2_p3
                    )
                 )
            )

    return angle

def get_overshoot_pos(
        cp_rel, pod, pod_heading, angle):

    """ Get the point where the current heading will overshoot the target
    """

    d_overshoot_target = abs(cp_rel.d * math.tan(abs(angle)))

    # the d between pod and the overshoot point.
    d_pod_overshoot = math.hypot(cp_rel.d, d_overshoot_target)

    # coordinates of overshoot relative to pod

    x_overshoot = (d_pod_overshoot * math.cos(pod_heading))
    y_overshoot = (d_pod_overshoot * math.sin(pod_heading))

    relative_overshoot = point(
        pod.pos.x + x_overshoot, pod.pos.y - y_overshoot)

    global_overshoot = relative_overshoot - cp_rel.parent_cp.pos

    return global_overshoot


def left_or_right(p1, p2, p3):
    """ Determine whether from p1, passing p2
        to reach p3 will be a left or right turn """

    global_angle_p1_p2 = get_global_angle(p1, p2)
    global_angle_p2_p3 = get_global_angle(p2, p3)

    angle = get_signed_angle(global_angle_p1_p2, global_angle_p2_p3)

    if angle < 0:
        return "left"
    else:
        return "right"

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++INITIALIZATION++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

pods = {}

enemy_pods = {}

laps = int(input())
cp_count = int(input())

cps = {}
for i in range(cp_count):
    cp_x, cp_y = [int(j) for j in input().split()]
    cp_pos = point(cp_x, cp_y)
    cps[i] = cp(cp_pos, i)

counter = 0
last_shield_activation = [0, 0]

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++GAME LOOP++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++

while True:
    counter += 1
    for i in range(2):

        x, y, global_vx, global_vy, angle_facing, current_cp_id = [
            int(j) for j in input().split()]
        print(f"pod {i}", end=" ", file=sys.stderr)
        angle_facing = flip_rotation_direction(angle_facing, "degrees")

        angle_facing += 5  # original angle seems to be off by 5 degrees
        angle_facing = change_angle_scale_to_180(angle_facing)
        angle_facing_in_rads = degree_to_rads(angle_facing)

        pod_pos = point(x, y)
        pod_vector = vector(global_vx, global_vy)
        current_cp = cps[current_cp_id]
        current_pod = pod(pod_pos, pod_vector, angle_facing_in_rads, current_cp)
        current_pod.get_heading()
        
        #if i == 1 and counter < 10:
        #    current_pod.thrust = 10

        current_pod.predict_next_pos()

        pods[i] = current_pod

    for i in range(2):
        # OPPONENT
        x_2, y_2, global_vx_2, global_vy_2, angle_2, current_check_point_id_2 = [int(j) for j in input().split()]

        print(f"enemy_pod {i}", file=sys.stderr)
        angle_facing = flip_rotation_direction(angle_2, "degrees")

        angle_facing += 5  # original angle seems to be off by 5 degrees
        angle_facing = change_angle_scale_to_180(angle_facing)
        angle_facing_in_rads = degree_to_rads(angle_facing)

        pod_pos = point(x_2, y_2)
        pod_vector = vector(global_vx_2, global_vy_2)
        current_cp = cps[current_check_point_id_2]
        current_pod = pod(pod_pos, pod_vector, angle_facing_in_rads, current_cp)
        current_pod.predict_next_pos()
        enemy_pods[i] = current_pod


    # collisions
    collision_rg = 700
    if counter > 10:
        for p in pods.keys():
            print(f"pod: {p} ", file=sys.stderr)
            print(f"counter: {counter} ", file=sys.stderr)
            print(f"last_shield_activation: {last_shield_activation[p]} ", file=sys.stderr)
            for ep in enemy_pods.keys():
                x_diff = abs(pods[p].next_pos.x - enemy_pods[ep].next_pos.x)
                y_diff = abs(pods[p].next_pos.y - enemy_pods[ep].next_pos.y)
                if (
                        abs(pods[p].next_pos.x - enemy_pods[ep].next_pos.x) < collision_rg and
                        abs(pods[p].next_pos.y - enemy_pods[ep].next_pos.y) < collision_rg):
                    if counter - last_shield_activation[p] > 15:
                        pods[p].thrust = "SHIELD"
                        last_shield_activation[p] = counter

    print(f"{pods[0].heading.x} {pods[0].heading.y} {pods[0].thrust}")
    print(f"{pods[1].heading.x} {pods[1].heading.y} {pods[1].thrust}")
