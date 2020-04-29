import sys
import math

# Setting up landing plane
target_x1 = 0
target_y1 = 0
target_x2 = 0
target_y2 = 0

last_x = 0
last_y = 0

found = False

# the number of points used to draw the surface of Mars.
surface_n = int(input())
for i in range(surface_n):
    # land_x: X coordinate of a surface point. (0 to 6999)
    # land_y: Y coordinate of a surface point. By linking all the points together in a sequential fashion, you form the surface of Mars.
    land_x, land_y = [int(j) for j in input().split()]

    if last_y == land_y and found == False:
        target_x1 = last_x
        target_y1 = last_y
        target_x2 = land_x
        target_y2 = land_y
        found == True
    #print("x: " + str(land_x) + "  y: " + str(land_y), file=sys.stderr)
    last_x = land_x
    last_y = land_y


# game loop
counter = 0
stage = 1
approach_from = ''
while True:
    counter += 1
    print("counter: " + str(counter), file=sys.stderr)
    print(f"land target x: {target_x1},{target_x2}", file=sys.stderr)

    # h_speed: the horizontal speed (in m/s), can be negative.
    # v_speed: the vertical speed (in m/s), can be negative.
    # fuel: the quantity of remaining fuel in liters.
    # rotate: the rotation angle in degrees (-90 to 90).
    # power: the thrust power (0 to 4).
    x, y, h_speed, v_speed, fuel, rotate, power = [
        int(i) for i in input().split()]

# v = d/t

    angle = 0

    print(f"approach from {approach_from}", file=sys.stderr)
    # FIRST STAGE
    if stage == 1:
        thrust = 4
        if x < target_x1:
            approach_from = "left"
            angle = -25  # go right
            if abs(h_speed) > 30:
                angle = 0
                stage = 2
        elif x > target_x2:
            approach_from = "right"
            angle = 25  # go left
            if abs(h_speed) > 30:
                angle = 0
                stage = 2

    elif stage == 2:

        thrust = 3

        if approach_from == "left" and x - 50 > target_x1:
            stage = 3
        if approach_from == "right" and x + 50 < target_x2:
            stage = 3

    elif stage == 3:

        thrust = 4

        if abs(h_speed) > 1:
            if h_speed > 1:
                angle = 70
            if h_speed < 1:
                angle = -70
        else:
            angle = 0
            stage = 4

    elif stage == 4:

        if v_speed < -4:
            thrust = 4
        if v_speed > -1:
            thrust = 3

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # rotate power. rotate is the desired rotation angle. power is the desired thrust power.
    print("stage: " + str(stage), file=sys.stderr)
    print(str(angle) + " " + str(thrust))
