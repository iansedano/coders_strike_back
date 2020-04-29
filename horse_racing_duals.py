import sys
import math
import bisect

n = int(input())
horses = []
max_pi = 0

for i in range(n):
    idx, pi = i, int(input())
    bisect.insort(horses, pi)

min_diff = 50
checked = []

for i in range(1, len(horses)):
    diff = horses[i] - horses[i - 1]
    if diff < min_diff:
        min_diff = diff

print(min_diff)