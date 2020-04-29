import sys
import math

# drawing surface ang getting target plane
target_x1, target_y1, target_x2, target_y2 = 0, 0, 0, 0
last_x, last_y = 0, 0
surface_n = int(input())
for i in range(surface_n):
    land_x, land_y = [int(j) for j in input().split()]
    if last_y == land_y:
        target_x1 = last_x
        target_y1 = last_y
        target_x2 = land_x
        target_y2 = land_y
    last_x = land_x
    last_y = land_y


# game loop
stage = 1
approach_from = ''
counter = 0

while True:
    counter += 1
    # print("counter: " + str(counter), file=sys.stderr)
    # print(f"land target x: {target_x1},{target_x2}", file=sys.stderr)
    # print(f"land target y: {target_y1}", file=sys.stderr)

    x, y, h_speed, v_speed, fuel, rotate, power = [
        int(i) for i in input().split()]

    # trajectory calculation

    if v_speed > 0:
        v_speed *= -1


    if h_speed != 0 and v_speed != 0:
        aoa = math.atan2(v_speed, h_speed)
        print(f"aoa {round(math.degrees(aoa), 3)} degrees", file=sys.stderr)

        y0 = y - target_y1  # height from target
        # print(f"y0 {y0}", file=sys.stderr)

        vector_mag = math.hypot(h_speed, v_speed)

        theta = aoa

        g = 3.711

        distance = (
            (vector_mag**2 / 2 * g) *
            (
                1 + (
                    1 + (
                        (2 * g * y0) / (
                            vector_mag**2 * math.sin(theta)**2)
                    )
                ) ** 0.5
            )
        ) * (math.sin(2 * theta))

        distance = (int(distance) / 10) * -1


        print(f"projected landing distance {distance}", file=sys.stderr)

    angle = 0

    # FIRST STAGE

    if stage == 1:
        thrust = 4
        if x < target_x1:
            approach_from = "left"
            angle = -40  # go right
            if abs(h_speed) > 40:
                stage = 2
        elif x > target_x2:
            approach_from = "right"
            angle = 40  # go left
            if abs(h_speed) > 40:
                stage = 2

    elif stage == 2:
        angle = 0
        if counter % 20 == 0:
            thrust = 3
        else:
            thrust = 4

        comp_dist_l = int( (distance * 0.3) * abs(h_speed * 0.01) )
        comp_dist_r = int( (distance * 0.3) * abs(h_speed * 0.01) )

        print(f"comp dist right {comp_dist_r}", file=sys.stderr)

        if approach_from == "left" and comp_dist_l + x > target_x1:

            print(f"comp dist {comp_dist_l}", file=sys.stderr)
            stage = 3

        if approach_from == "right" and comp_dist_r + x < target_x2:

            print(f"comp dist {comp_dist_r}", file=sys.stderr)
            stage = 3

    elif stage == 3: # SLOW DOWN

        thrust = 4

        opp_aoa = int((math.degrees(aoa) - 90) % 360 - 180)


        print(f"opp ang of atk {opp_aoa}", file=sys.stderr)

        if opp_aoa >= 70:
            opp_aoa = 70
        if opp_aoa <= -70:
            opp_aoa = -70

        if abs(h_speed) > 1:
            if h_speed > 1:
                angle = opp_aoa
            if h_speed < 1:
                angle = opp_aoa
        else:
            angle = 0
            stage = 4

    elif stage == 4:

        if v_speed < -30:
            thrust = 4
        else:
            thrust = 3



    # rotate power. rotate is the desired rotation angle. power is the desired thrust power.
    print("stage: " + str(stage), file=sys.stderr)
    print(str(angle) + " " + str(thrust))
