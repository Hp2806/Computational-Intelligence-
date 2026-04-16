import random

def display_grid(size, agent=None, gold=None, wumpus=None, pits=[], wumpus_alive=True, reveal_all=False):
    print("\nGrid Display:")
    for r in range(size, 0, -1):
        row_display = ""
        for c in range(1, size + 1):
            pos = (r, c)
            if pos == agent:
                row_display += " A "
           
            elif reveal_all:
                if pos == gold:
                    row_display += " G "
                elif pos == wumpus:
                    row_display += " W " if wumpus_alive else " x "
                elif pos in pits:
                    row_display += " P "
                else:
                    row_display += " . "
            else:
                row_display += " . "
        print(row_display)
    print()

def get_coord(label, size, occupied_list=[]):
    while True:
        try:
            print(f"Set position for {label}:")
            r = int(input(f"  Enter row (1-{size}): "))
            c = int(input(f"  Enter column (1-{size}): "))
            pos = (r, c)
            if not (1 <= r <= size and 1 <= c <= size):
                print(f"  Error: Position must be within 1 and {size}.")
                continue
            if pos in occupied_list:
                print("  Error: This position is already taken. Choose another.")
                continue
            return pos
        except ValueError:
            print("  Invalid input. Please enter integers.")
while True:
    try:
        GRID_SIZE = int(input("Enter grid size: "))
        if GRID_SIZE >= 2:
            break
        print("Grid size must be at least 2.")
    except ValueError:
        print("Invalid input.")
gold_position = get_coord("GOLD", GRID_SIZE)
wumpus_position = get_coord("WUMPUS", GRID_SIZE, [gold_position])
agent_position = get_coord("AGENT", GRID_SIZE, [gold_position, wumpus_position])
pits = []
while True:
    #display_grid(GRID_SIZE, agent_position, gold_position, wumpus_position, pits, reveal_all=True)
    choice = input("Add a PIT? (y/n): ").strip().lower()
    if choice == 'y':
        occupied = [gold_position, wumpus_position, agent_position] + pits
        new_pit = get_coord("PIT", GRID_SIZE, occupied)
        pits.append(new_pit)
    elif choice == 'n':
        break
    else:
        print("Invalid choice. Enter 'y' or 'n'.")

print("\n" + "="*30)
print("ENVIRONMENT STARTED.")
print("="*30)

visited = set()
path_taken = [agent_position]

def get_sensors(pos, wumpus_alive):
    row, col = pos
    stench, breeze, glitter = None, None, None
    directions = [(0,1), (0,-1), (1,0), (-1,0)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 1 <= r <= GRID_SIZE and 1 <= c <= GRID_SIZE:
            if (r, c) == wumpus_position and wumpus_alive:
                stench = "STENCH"
            if (r, c) in pits:
                breeze = "BREEZE"
    if pos == gold_position:
        glitter = "GLITTER"
    return stench, breeze, glitter
print("------ WUMPUS WORLD START ------")
current = agent_position
wumpus_alive = True
bump_sensor = None
scream_sensor = None
has_arrow = True
step_count = 1

while True:
    visited.add(current)
    display_grid(GRID_SIZE, current, gold_position, wumpus_position, pits, wumpus_alive, reveal_all=False)
    
    stench, breeze, glitter = get_sensors(current, wumpus_alive)

    if current in pits:
        print(f"Step {step_count} at {current} -> [None, BREEZE, None, None, None]")
        print("\nGAME OVER: Agent fell in a pit and died.")
        break
    if current == wumpus_position and wumpus_alive:
        print(f"Step {step_count} at {current} -> [STENCH, None, None, None, None]")
        print("\nGAME OVER: Agent eaten by the Wumpus.")
        break
    if glitter == "GLITTER":
        print(f"Step {step_count} at {current} -> [None, None, GLITTER, None, None]")
        print("\nSUCCESS! Gold found safely.")
        break

    print(f"Step {step_count} at {current} -> "
          f"[{stench or 'None'}, {breeze or 'None'}, {glitter or 'None'}, "
          f"{bump_sensor or 'None'}, {scream_sensor or 'None'}]")

    bump_sensor = None
    scream_sensor = None
    action = input("Enter action (up/down/left/right/shoot): ").strip().lower()

    if action == "shoot":
        if not has_arrow:
            print("Arrow already used!")
            continue
        direction = input("Enter shoot direction (up/down/left/right): ").strip().lower()
        dr, dc = 0, 0
        if direction == 'up': dr, dc = 1, 0
        elif direction == 'down': dr, dc = -1, 0
        elif direction == 'right': dr, dc = 0, 1
        elif direction == 'left': dr, dc = 0, -1
        else:
            print("Invalid direction.")
            continue

        has_arrow = False
        hit = False
        r, c = current[0] + dr, current[1] + dc
        while 1 <= r <= GRID_SIZE and 1 <= c <= GRID_SIZE:
            if (r, c) == wumpus_position:
                hit = True
                break
            r += dr
            c += dc
        if hit and wumpus_alive:
            wumpus_alive = False
            scream_sensor = "SCREAM"
            print("--- SCREAM! The Wumpus is dead! ---")
        else:
            print("The arrow missed.")
        step_count += 1

    elif action in ['up', 'down', 'left', 'right']:
        dr, dc = 0, 0
        if action == 'up': dr, dc = 1, 0
        elif action == 'down': dr, dc = -1, 0
        elif action == 'right': dr, dc = 0, 1
        elif action == 'left': dr, dc = 0, -1

        new_r, new_c = current[0] + dr, current[1] + dc
        if 1 <= new_r <= GRID_SIZE and 1 <= new_c <= GRID_SIZE:
            current = (new_r, new_c)
            path_taken.append(current)
        else:
            bump_sensor = "BUMP"
            print("You hit the wall.")
        step_count += 1
    else:
        print("Invalid action.")

# Final reveal
display_grid(GRID_SIZE, current, gold_position, wumpus_position, pits, wumpus_alive, reveal_all=True)
print("\nPath explored:", path_taken)
print("------ GAME OVER ------")
