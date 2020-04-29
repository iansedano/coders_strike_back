import sys
import math

# w: width of the building.
# h: height of the building.

building_w, building_h = [int(i) for i in input().split()]

n = int(input())  # maximum number of turns before game over.

current_x, current_y = [int(i) for i in input().split()]
target_x, target_y = 0, 0

search_w = building_w
search_h = building_h

aimed_change_x = 0
aimed_change_y = 0

cycle = 0

while True:
    # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)
    bomb_dir = input()

    if cycle == 0:
        if "U" in bomb_dir:
            search_h = current_y
            bottom_lim = current_y
        if "R" in bomb_dir:
            search_w = building_w - current_x - 1
            left_lim = current_x
        if "D" in bomb_dir:
            search_h = building_h - current_y - 1
            top_lim = current_y
        if "L" in bomb_dir:
            search_w = current_x
            right_lim = current_x
    cycle = 1

    if "U" in bomb_dir:
        aimed_change_y = math.floor((search_h / 2) * -1)
        target_y = int(current_y + aimed_change_y)
        search_h += aimed_change_y

    if "R" in bomb_dir:
        aimed_change_x = math.ceil(search_w / 2)
        target_x = int(current_x + aimed_change_x)
        search_w -= aimed_change_x

    if "D" in bomb_dir:
        aimed_change_y = math.ceil(search_h / 2)
        target_y = int(current_y + aimed_change_y)
        search_h -= aimed_change_y

    if "L" in bomb_dir:
        aimed_change_x = math.floor((search_w / 2) * -1)
        target_x = int(current_x + aimed_change_x)
        search_w += aimed_change_x

    instruction_x = int(target_x)
    instruction_y = int(target_y)

    current_x = target_x
    current_y = target_y

    # the location of the next window Batman should jump to.
    print(f"{instruction_x} {instruction_y}")