import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways
n, l, e = [int(i) for i in input().split()]

nodes = {}
for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in input().split()]
    nodes[j] = {1:n1, 2:n2}

gateways = []
for i in range(e):
    ei = int(input())  # the index of a gateway node
    gateways.append[]

print(nodes, file=sys.stderr)



# game loop
while True:
    si = int(input())  # The index of the node on which the Skynet agent is positioned this turn

    node_to_cut = ''

    for i in nodes.Keys:
        for j in nodes[l].Keys:


    


    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)


    # Example: 0 1 are the indices of the nodes you wish to sever the link between
    print(node_to_cut)
