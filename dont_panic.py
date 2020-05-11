
class Clone:
    def __init__(self, floor, pos):
        self.floor = floor
        self.pos = pos
        self.action = "WAIT"
        self.direction = ""
        self.instructions_done = -3

    def block(self):
        self.action = "BLOCK"
        instructions_to_next_clone.append("WAIT")

    def wait(self):
        self.action = "WAIT"
        instructions_to_next_clone.append("WAIT")

    def check_elevators(self):
        for e in elevators:
            if self.floor == e[0]:
                if self.pos > e[1] and self.direction == "RIGHT":
                    return True
                elif self.pos < e[1] and self.direction == "LEFT":
                    return True
        return False

    def check_exit(self):
        if self.floor == exit_floor:
            if self.pos > exit_pos and self.direction == "RIGHT":
                return True
            elif self.pos < exit_pos and self.direction == "LEFT":
                return True
        return False


elevators = []
clones = []
counter = -1
instructions_to_next_clone = []

nb_floors, width, nb_rounds, exit_floor, exit_pos, nb_total_clones, nb_additional_elevators, nb_elevators = [int(i) for i in input().split()]
for i in range(nb_elevators):
    elevator_floor, elevator_pos = [int(j) for j in input().split()]
    elevators.append([elevator_floor, elevator_pos])

while True:
    counter += 1
    clone_floor, clone_pos, direction = input().split()
    clone_floor = int(clone_floor)
    clone_pos = int(clone_pos)

    if counter % 3 == 0:
        new_clone = Clone(clone_floor, clone_pos)
        clones.append(new_clone)

    try:
        leading_clone = clones[0]
        leading_clone.floor = clone_floor
        leading_clone.pos = clone_pos
        leading_clone.direction = direction

        for c in clones:
            c.instructions_done += 1

        if leading_clone.instructions_done < len(instructions_to_next_clone):
            leading_clone.action = "WAIT"
        elif leading_clone.check_elevators():
            leading_clone.block()
        elif leading_clone.check_exit():
            leading_clone.block()
        else:
            leading_clone.wait()

        print(leading_clone.action)
        if leading_clone.action == "BLOCK":
            clones.pop(0)
    except:
        print("WAIT")
