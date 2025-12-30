from dlu.shaper import *
import math

ROWS = 6
COLS = 11
MASKS = [1 << col for col in range(COLS)]
BORDER = "  " + '=' * (COLS * 2 - 1)
ONE_BOARD = (-1, -1)
NO_BOARDS = (-1, -2)
CPS = (10**5,          5*10**5,
       10**6, 2*10**6, 5*10**6,
       10**7, 2*10**7, 5*10**7,
       10**8)
CHECKPOINTS = ("    100,000",                "    500,000",
               "  1,000,000", "  2,000,000", "  5,000,000",
               " 10,000,000", " 20,000,000", " 50,000,000",
               "100,000,000")
               

########

def insert(board, form, row, col):
    new_board = board.copy()
    for tile in form:
        t_row = row + tile[0]
        t_col = col + tile[1]
        if not (0 <= t_row < ROWS and 0 <= t_col < COLS):
            return False
        if board[t_row] & MASKS[t_col]:
            return False
        new_board[t_row] |= MASKS[t_col]
    return new_board

def make_rows(tiles):
    grid = [0] * ROWS
    for tile in tiles:
        grid[tile[0]] |= MASKS[tile[1]]
    return [(i, grid[i]) for i in range(ROWS) if grid[i]]

def generate_boards(board, shapes, hits, misses):
    hit_rows = make_rows(hits)
    miss_rows = make_rows(misses)

    counter = 0
    cp = 0
    def generate(board, shapes):
        if not shapes:
            for hit_row in hit_rows:
                if ~board[hit_row[0]] & hit_row[1]:
                    return []

            nonlocal counter, cp
            counter += 1
            if counter == CPS[cp]:
                print(f" {CHECKPOINTS[cp]} made")
                cp += 1
            return [board]

        boards = []
        forms = shapes[0]
        remain = shapes[1:]
        for form in forms:
            for row in range(ROWS):
                for col in range(COLS):
                    new_board = insert(board, form, row, col)
                    if not new_board:
                        continue
                    for miss_row in miss_rows:
                        if new_board[miss_row[0]] & miss_row[1]:
                            break
                    else:
                        boards.extend(generate(new_board, remain))
        return boards
    return generate(board, shapes)

########

class Boards:
    def __init__(self, shapes, hits, misses):
        self.fixed = [0] * ROWS
        self.boards = generate_boards(self.fixed, shapes, hits, misses)
        self.shapes = shapes
        self.hits = hits
        self.misses = misses

    # due to symmetry, we can quarter the time taken
    def get_first_counts(self):
        cols_2 = math.ceil(COLS / 2)
        rows_2 = math.ceil(ROWS / 2)
        counts = [[0] * cols_2 for _ in range(rows_2)]

        for board in self.boards:
            for row in range(rows_2):
                for col in range(cols_2):
                    if board[row] & MASKS[col]:
                        counts[row][col] += 1
        return counts

    def get_counts(self):
        counts = [[0] * COLS for _ in range(ROWS)]

        for board in self.boards:
            for row in range(ROWS):
                for col in range(COLS):
                    if board[row] & MASKS[col]:
                        counts[row][col] += 1
        return counts

    def best_move(self, counts):
        total = len(self.boards)
        if total == 0:
            return NO_BOARDS
        if total == 1:
            return ONE_BOARD

        # for a binary outcome, entropy is maxed at p = 1/2
        best = total + 1
        move = NO_BOARDS
        for row in range(len(counts)):
            for col in range(len(counts[row])):
                d = counts[row][col] * 2 - total
                if d == 0:
                    return (row, col)
                delta = abs(d)
                if delta < best or d == best:
                    best = delta
                    move = (row, col)
        return move

    def most_move(self, counts):
        total = len(self.boards)
        if total == 0:
            return NO_BOARDS
        if total == 1:
            return ONE_BOARD

        # this minimizes misses, as a miss will reduce the pool greatly
        best = -1
        move = NO_BOARDS
        for row in range(len(counts)):
            for col in range(len(counts[row])):
                if (row, col) in self.hits or (row, col) in self.misses:
                    continue
                count = counts[row][col]
                if count == total:
                    return (row, col)
                if count > best:
                    best = count
                    move = (row, col)
        return move

    def already_hitmiss(self, tile):
        return tile in self.hits or tile in self.misses

    def add_hit(self, tile):
        if self.already_hitmiss(tile):
            return False
        self.hits.append(tile)
        self.boards = list(filter(lambda b: b[tile[0]] & MASKS[tile[1]],
                                  self.boards))
        return True

    def add_miss(self, tile):
        if self.already_hitmiss(tile):
            return False
        self.misses.append(tile)
        self.boards = list(filter(lambda b: not (b[tile[0]] & MASKS[tile[1]]),
                                  self.boards))
        return True

    #TODO
    def fix_shape(self, shape, form, origin):
        if shape not in shapes:
            return False
        if not 0 <= form < len(shape):
            return False
        new_board = insert(self.fixed, shape[form], *origin)
        if not new_board:
            return False
        self.fixed = new_board
        self.shapes.remove(shape)
        self.boards = generate_boards(self.fixed, self.shapes,
                                      self.hits, self.misses)
        return True
    
        
