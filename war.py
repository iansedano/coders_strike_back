import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

deck_p1 = []
deck_p2 = []

n = int(input())  # the number of cards for player 1

def convert_faces(card):
    if card == "A":
        return 14
    elif card == "K":
        return 13
    elif card == "Q":
        return 12
    elif card == "J":
        return 11
    else:
        return card

for i in range(n):
    cardp_1 = input()[:-1]  # the n cards of player 1
    cardp_1 = convert_faces(cardp_1)
    deck_p1.append(cardp_1)
m = int(input())  # the number of cards for player 2
for i in range(m):
    cardp_2 = input()[:-1]  # the m cards of player 2
    cardp_2 =  convert_faces(cardp_2)
    deck_p2.append(cardp_2)

print(deck_p1, file=sys.stderr)
print(deck_p2, file=sys.stderr)

turn = 1

war_deck = []

def battle():
    if deck_1[-1] > deck_2[-1]:
        deck_1.insert(0, deck_1.pop(-1))
        deck_1.insert(0, deck_2.pop(-1))
        return 1
    
    elif deck_1[-1] < deck_2[-1]:
        deck_2.insert(0, deck_1.pop(-1))
        deck_2.insert(0, deck_1.pop(-1))
        return 2

    elif deck_1[-1] == deck_2[-1]:
        war_deck.append(deck_p1.pop(-1))
        war_deck.append(deck_p1.pop(-1))
        war_deck.append(deck_p1.pop(-1))
        war_deck.append(deck_p1.pop(-1))
        war_deck.append(deck_p2.pop(-1))
        war_deck.append(deck_p2.pop(-1))
        war_deck.append(deck_p2.pop(-1))
        war_deck.append(deck_p2.pop(-1))
        return 3

while True:
    print(f"turn {turn}", file=sys.stderr)
    print(f"p1 card {deck_p1[-1]}", file=sys.stderr)
    print(f"p2 card {deck_p2[-1]}", file=sys.stderr)

    battle()

    if len(deck_p1) == 0 or len(deck_p2) == 0:
        break

    print(f"deck_p1 {len(deck_p1)} deck_p2 {len(deck_p2)}", file=sys.stderr)    
    
    turn += 1

if deck_p1 > deck_p2:
    winner = 1
else:
    winner = 2

print(f"{winner} {turn}")
