import sys
import math

# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways
n, l, e = [int(i) for i in input().split()]

nodes = {}
for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in input().split()]
    nodes[i] = {1:n1, 2:n2}

gateways = []
for i in range(e):
    ei = int(input())  # the index of a gateway node
    gateways.append(ei)

print(gateways, file=sys.stderr)
print(nodes, file=sys.stderr)

critical_nodes=[]
for g in gateways:
    print(f"g {g}", file=sys.stderr)
    for n in nodes.keys():
        if nodes[n][1] == int(g) or nodes[n][2] == int(g):
            critical_nodes.append(n)

print(critical_nodes, file=sys.stderr)

# game loop
while True:
    si = int(input())  # The index of the node on which the Skynet agent is positioned this turn
    print(f"si {si}", file=sys.stderr)
    
    node_to_cut = ''

    for cn in critical_nodes:
        if nodes[cn][1] == si or nodes[cn][2] == si:
            node_to_cut = nodes[cn]
            critical_nodes.remove(cn)
    

    for cn in critical_nodes:
        if node_to_cut == '':
            node_to_cut = nodes[critical_nodes[0]]
            critical_nodes.pop(0)
    
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)


    # Example: 0 1 are the indices of the nodes you wish to sever the link between
    print(f"{node_to_cut[1]} {node_to_cut[2]}")
