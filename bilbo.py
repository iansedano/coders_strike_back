import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

magic_phrase = input()

#print(magic_phrase, file=sys.stderr)

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

instructions = []

length = len(magic_phrase)
a = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "

for l in magic_phrase:
    instructions.append(">")
    letter_index = a.index(l)
    while letter_index > 0:
        instructions.append("+")
    instructions.append(".")

#print(instructions, file=sys.stderr)

instructions_to_print = ""

for i in instructions:
    instructions_to_print = instructions_to_print + i
    
#print(instructions_to_print, file=sys.stderr)

print(">+.")