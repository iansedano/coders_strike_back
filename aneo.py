import sys
import math

speed_lim = int(input()) # in km/h
light_count = int(input())
lights = {}
for i in range(light_count):
    distance, duration = [int(j) for j in input().split()]
    lights[i] = {'d':distance, 'dur':duration}


speed_to_try = speed_lim
while True:
    current_set = True
    for l in lights.keys():
        time_to_light = lights[l]['d'] / (speed_to_try / 3.6)
        if (int(round(time_to_light,2)) // lights[l]['dur']) % 2 != 0:
            current_set = False
            break
    if current_set == True:
        break
    else:
        speed_to_try -= 1

print(speed_to_try)
