import sys
import math

# Don't let the machines win. You are humanity's last hope...

width = int(input())  # the number of cells on the X axis
height = int(input())  # the number of cells on the Y axis

nodes = []
for i in range(height):
    line = input()  # width characters, each either 0 or .
    for j, c in enumerate(line):
        if c == '0':
            nodes.append([j, i])

for n in nodes:
    out_string = ''
    # right
    rx = n[0] + 1
    ry = n[1]
    right = [rx, ry]
    # down
    dx = n[0]
    dy = n[1] + 1
    down = [dx, dy]

    out_string += f"{n[0]} {n[1]} "

    while rx <= width:
        found_r = False
        if right in nodes:
            out_string += f"{right[0]} {right[1]} "
            found_r = True
            break
        else:
            rx += 1
            right = [rx, ry]

    if found_r is False:
        out_string += "-1 -1 "


    while dy <= height:
        found_d = False
        if down in nodes:
            out_string += f"{down[0]} {down[1]}"
            found_d = True
            break
        else:
            dy += 1
            down = [dx, dy]
        
    if found_d is False:
        out_string += "-1 -1"

    print(out_string, end="\n")


