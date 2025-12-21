from dlu.shaper import *
import math

ROWS = 6
COLS = 11
MASKS = [1 << col for col in range(COLS)]
BORDER = "  " + '=' * (COLS * 2 - 1)
ONE_BOARD = (-1, -1)
NO_BOARDS = (-1, -2)

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
    grid = [0 for row in range(ROWS)]
    for tile in tiles:
        grid[tile[0]] |= MASKS[tile[1]]
    return [(i, grid[i]) for i in range(ROWS) if grid[i]]

def generate_boards(shapes, hits, misses):
    hit_rows = make_rows(hits)
    miss_rows = make_rows(misses)

    #COUNTER = 0
    #CHECKPOINTS = (1e5, 5e5, 1e6, 2e6, 5e6, 1e7)

    def generate(board, shapes):
        if not shapes:
            for hit_row in hit_rows:
                if ~board[hit_row[0]] & hit_row[1]:
                    return []
            #Boards.COUNTER += 1
            #if Boards.COUNTER in Boards.CHECKPOINTS:
            #    print(f"  Currently at {Boards.COUNTER} boards.")
            return [board]

        boards = []
        forms = shapes[0][0]
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
    return generate([0 for row in range(ROWS)], shapes)

########

class Boards:
    def __init__(self, shapes, hits, misses):
        self.boards = generate_boards(shapes, hits, misses)
        self.copies = 1
        for shape in shapes:
            self.copies *= shape[1]
        self.hits = hits
        self.misses = misses

    def get_counts(self):
        counts = [[0 for col in range(COLS)]
                  for row in range(ROWS)]

        for board in self.boards:
            for row in range(ROWS):
                for col in range(COLS):
                    if not (board[row] & MASKS[col]):
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
        for row in range(ROWS):
            for col in range(COLS):
                d = counts[row][col] * 2 - total
                if d == 0:
                    return (row, col)
                delta = abs(d)
                if delta < best or d == best:
                    best = delta
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
