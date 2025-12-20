from dlu.snowdown import *
import time

def print_board(board):
    print(BORDER)
    for row in board:
        row_str = ['X' if b == '1' else '.' for b in \
                   bin(row)[-1:1:-1].ljust(COLS, '0')]
        print("  " + ' '.join(row_str))
    print(BORDER)
    print()


def next_move(state):
    print("Getting counts...")
    start = time.time()
    counts = state.get_counts()

    print("Finding best move...")
    move = state.best_move(counts)
    dur = round(time.time() - start, 3)

    if move == NO_BOARDS:
        print("You (not I) dun goofed somewhere. There are 0 possible boards.")
        return False
    if move == ONE_BOARD:
        print("Only one possible board:")
        print_board(state.boards[0])
        return False

    best_count = counts[move[0]][move[1]]
    p = round(best_count/len(state.boards), 5)
    delta = abs(best_count - len(state.boards) / 2)
    print(f"The best move is {move} with p = {p} / d  = {delta}" +\
          f" [{int(delta * state.copies)}]). Found in {dur}s.\n")
    return True


def check_move(abc):
    try:
        xyz = [int(a) for a in abc.split(' ')]
    except ValueError:
        print("That's not in the right format >:(")
        return False

    try:
        x, y, z = xyz
    except ValueError:
        print(f"len(xyz) arguments found instead of three >:(")
        return False

    if x < 0 or x >= ROWS:
        print(f"X = {x} is out of range >:(")
        return False
    if y < 0 or y >= COLS:
        print(f"Y = {y} is out of range >:(")
        return False
    if z not in (0, 1):
        print(f"Z = {z} is not 0 or 1 >:(")
        return False

    return True


def check_check(a):
    try:
        x = int(a)
    except ValueError:
        print("That's literally not a number wth.")
        return False

    if x not in (0, 1):
        print("Follow instructions can or not.")
        return False

    return True


def print_hitmiss(hits, misses, *highlight):
    states = [["." for col in range(COLS)]
             for row in range(ROWS)]
    for hit in hits:
        states[hit[0]][hit[1]] = '1'
    for miss in misses:
        states[miss[0]][miss[1]] = '0'
    if highlight:
        x, y, z = highlight
        states[x][y] = ('o', 'i')[z]

    print(BORDER)
    for state in states:
        print("  " + ' '.join(state))
    print(BORDER)


def ask_move(state):
    print("Please input your new move in the form:\n    'X Y Z'")
    print("where\n  X is the row from the top (0-indexing)")
    print("  Y is the column from the left (0-indexing)")
    print("  Z is 0 for a miss or 1 for a hit")

    while True:
        abc = input("New move:\n")
        while not check_move(abc):
            abc = input("\nTry again bodoh:\n")

        x, y, z = [int(a) for a in abc.split(' ')]
        print(f"\n--> {'HIT' if z else 'MISS'} at ({x},{y})")
        print_hitmiss(state.hits, state.misses, x, y, z)
        correct = input("Is this correct? 1 for YES, 0 for NO.\n")
        while not check_check(correct):
            correct = input("Come, practice your literacy again:\n")

        if int(correct):
            break
        else:
            print("\nStupiak lah you.")

    return (x, y, z)


def print_state(state, with_board):
    num_boards = len(state.boards)
    if with_board:
        print_hitmiss(state.hits, state.misses)
    print(f"{'' if  with_board else '  '}Possible boards: {num_boards}" +\
          f" [{num_boards * state.copies}]")
    print(f"{'' if  with_board else '  '}Roughly" +\
          f" {round(math.log(num_boards, 2))} more steps for full info.\n")


def do_move(state):
    *tile, hit = ask_move(state)
    if state.already_hitmiss(tile):
        print(f"{tile} has already been checked:")
        print_hitmiss(state.hits, state.misses)
        print("If this was a mistake with the latest input (as expected" +\
              " from the buffoon you are), you may try again. Otherwise," +\
              " you may have to restart lol l00ser.\n\n")
        return do_move(state)

    print("\nUpdating possible boards...")
    start = time.time()
    if hit:
        state.add_hit(tile)
    else:
        state.add_miss(tile)
    dur = round(time.time() - start, 3)
    print(f"Updated in {dur}s:")
    print_state(state, False)

########

def run(shapes, hits, misses):
    print(f"{sum(len(shape[0]) for shape in shapes)} forms" +\
          f" over {len(shapes)} shapes. Generating boards...")
    start = time.time()
    state = Boards(shapes, hits, misses)
    dur = round(time.time() - start, 3)
    print(f"Took {dur}s.")
    print_state(state, True)

    try:
        print("Press CTRL+C anytime to end the session" +\
              " and print the latest hits & misses.\n")
        while next_move(state):
            do_move(state)
    except KeyboardInterrupt:
        print("\nUser requested to end session.")

    # Just to print tuples without spaces
    hit_str = ", ".join(f"({hit[0]},{hit[1]})" for hit in state.hits)
    miss_str = ", ".join(f"({miss[0]},{miss[1]})" for miss in state.misses)
    print(f"To save for future use:\n  Hits:   [{hit_str}]\n" +\
          f"  Misses: [{miss_str}]\nIt's over! Hooray!")
