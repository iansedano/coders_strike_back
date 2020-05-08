"""
Coders Strike back Gold League Bot.

Currently standing in at around 960th place in gold league.

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


class cp:
    def __init__(self, pos, id):
        self.pos = pos
        self.id = id


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

    def add_compensation_angle(self, pod, limit=5000):
        """
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
        global_overshoot = get_global_translation_of_projection_crossover(
            self, pod, pod.vector.angle)

        # compensation values (point opposite target from overshoot)
        x_compensation = max(
                            min(int(-global_overshoot.x), limit), -limit)
        y_compensation = max(
                            min(int(-global_overshoot.y), limit), -limit)

        self.compensation = point(x_compensation, y_compensation)


class pod:
    def __init__(self, pos, global_vector, angle_facing, current_cp):
        self.pos = pos
        self.global_vector = global_vector
        self.angle_facing = angle_facing
        self.current_cp = current_cp
        self.next_cp = cps[(current_cp.id + 1) % (cp_count)]
        self.last_cp = cps[(current_cp.id - 1) % (cp_count)]
        self.vector = vector(self.global_vector.x, self.global_vector.y * -1)
        self.current_cp_rel = rel(self, self.current_cp)
        self.next_cp_rel = rel(self, self.next_cp)

    def get_heading(self):

        self.current_cp_rel.add_compensation_angle(self)
        self.heading = self.current_cp.pos + self.current_cp_rel.compensation

        self.thrust = 100

        if (
                self.current_cp_rel.d > 4000 and
                self.current_cp_rel.facing_offset < 1):
            self.thrust = "BOOST"

        if (
                self.vector.abs > 0 and
                abs(self.current_cp_rel.heading_offset) < 1):

            self.corner()

        facing_compensation(self)

    def prepare_corner(self):
        self.current_cp_rel.d
        self.global_vector
        self.current_cp_rel.d

        print(f"angle {round(self.angle_pod_current_next, 3)}", file=sys.stderr )

        prep_angle = pi / 5
        if self.angle_pod_current_next > 0:
            prep_angle *= -1

        prep_heading = get_global_translation_of_projection_crossover(
            self.current_cp_rel, self, pi/5)

    def corner(self):

        time_to_target = (self.current_cp_rel.d / self.vector.abs)

        self.angle_pod_current_next = get_angle_between_three_points(
            self.pos, self.current_cp.pos, self.next_cp.pos)

        self.next_cp_rel.add_compensation_angle(self)
        next_heading = (self.next_cp.pos + self.next_cp_rel.compensation)

        d_last_cp_current_cp = get_distance(self.last_cp.pos, self.next_cp.pos)
        half_way_point = d_last_cp_current_cp / 2

        if (
                self.current_cp_rel.d > half_way_point and
                self.current_cp_rel.heading_offset < 1):

            self.prepare_corner()

        if abs(self.angle_pod_current_next) > pi * 4/5:
            print(f"full speed", file=sys.stderr)
            if time_to_target < 6:
                self.heading = next_heading
                self.thrust = 100

        elif abs(self.angle_pod_current_next) > pi * 3/5:
            print(f"soft", file=sys.stderr)
            if time_to_target < 5.65:
                self.heading = next_heading
                self.thrust = 100

        elif abs(self.angle_pod_current_next) > pi * 2/5:
            print(f"90", file=sys.stderr)
            if time_to_target < 4:
                self.heading = next_heading
                self.thrust = 0

        elif abs(self.angle_pod_current_next) > pi * 1/5:
            print(f"hard", file=sys.stderr)
            if time_to_target < 6:
                self.heading = next_heading
                self.thrust = 0

        elif abs(self.angle_pod_current_next) < pi * 1/5:
            print(f"hairpin", file=sys.stderr)
            if time_to_target < 6:
                self.heading = next_heading
                self.thrust = 0



    def get_angle_to_next_cp(self):
        """
        Calculate where to aim to cut corner without missing target.

        Using the cp after the current target, calculate where
        in the current target, the pod should aim, so as to corner efficiently.
        Return an x and y coordinate.

        """
        x_between_current_and_next_cp = (
            self.current_cp.pos.x - self.next_cp.pos.x)
        y_between_current_and_next_cp = (
            self.current_cp.pos.y - self.next_cp.pos.y)

        d_between_current_and_next_cp = math.hypot(
            x_between_current_and_next_cp,
            y_between_current_and_next_cp
        )

        x_between_pod_and_next_cp = self.next_cp.pos.x - self.pos.x
        y_between_pod_and_next_cp = self.next_cp.pos.y - self.pos.y

        d_between_pod_and_next_cp = math.hypot(
            x_between_pod_and_next_cp,
            y_between_pod_and_next_cp)

        # law of cosines
        self.angle_pod_current_next = math.acos(
            (
                d_between_pod_and_next_cp ** 2 -
                self.current_cp_rel.d ** 2 -
                d_between_current_and_next_cp ** 2
            ) / (
                -2 * self.current_cp_rel.d *
                d_between_current_and_next_cp
            )
        )

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++FUNCTIONS++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++


def constrain(val, min_val, max_val):
    """Constrain value between min and max."""
    return min(max_val, max(min_val, val))


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


def get_distance(point1, point2):
    x = point2.x - point1.x
    y = point2.y - point1.y
    d = math.hypot(x, y)
    return d


def quad_from_pos(origin, target):
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


def get_relative_pos_from_global(p1, p2):
    quadrant = quad_from_pos(p1, p2)

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


def get_angle_between_three_points(p1, p2, p3):

    d_p1_p2 = get_distance(p1, p2)

    d_p2_p3 = get_distance(p2, p3)

    d_p1_p3 = get_distance(p1, p3)

    # law of cosines
    angle = (
        math.acos((
            d_p1_p3 ** 2 - d_p1_p2 ** 2 - d_p2_p3 ** 2
            ) / (-2 * d_p1_p2 * d_p2_p3))
        )

    return angle


def get_global_translation_of_projection_crossover(
        cp_rel, pod, angle):

    d_overshoot_target = abs(cp_rel.d * math.tan(abs(angle)))

    # the d between pod and the overshoot point.
    d_pod_overshoot = math.hypot(cp_rel.d, d_overshoot_target)

    # coordinates of overshoot relative to pod

    x_overshoot = (d_pod_overshoot * math.cos(pod.vector.angle))
    y_overshoot = (d_pod_overshoot * math.sin(pod.vector.angle))

    relative_overshoot = point(
        pod.pos.x + x_overshoot, pod.pos.y - y_overshoot)

    global_overshoot = relative_overshoot - cp_rel.parent_cp.pos

    return global_overshoot

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +++++++++++++++++++++GAME LOOP++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++


pods = {
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
    cp_pos = point(cp_x, cp_y)
    cps[i] = cp(cp_pos, i)

counter = 0


while True:
    counter += 1
    for i in range(2):

        x, y, global_vx, global_vy, angle_facing, current_cp_id = [
            int(j) for j in input().split()]

        angle_facing = flip_rotation_direction(angle_facing, "degrees")

        angle_facing += 5  # original angle seems to be off by 5 degrees
        angle_facing = change_angle_scale_to_180(angle_facing)
        angle_facing_in_rads = degree_to_rads(angle_facing)

        pod_pos = point(x, y)
        pod_vector = vector(global_vx, global_vy)
        current_cp = cps[current_cp_id]
        current_pod = pod(pod_pos, pod_vector, angle_facing_in_rads, current_cp)

        current_pod.get_heading()


        if i == 1 and counter < 10:
            current_pod.thrust = 10

        pods[i] = current_pod

    for i in range(2):
        # OPPONENT
        x_2, y_2, global_vx_2, global_vy_2, angle_2, current_check_point_id_2 = [int(j) for j in input().split()]

    print(f"{pods[0].heading.x} {pods[0].heading.y} {pods[0].thrust}")
    print(f"{pods[1].heading.x} {pods[1].heading.y} {pods[1].thrust}")
