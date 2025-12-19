from dlu.shaper import *
import math

ROWS = 6
COLS = 11
BORDER = "  " + '=' * COLS
ONE_BOARD = (-1, -1)
NO_BOARDS = (-1, -2)

class Board:
    def __init__(self):
        self.grid = tuple(tuple(False for col in range(COLS))
                          for row in range(ROWS))

    def can_insert(self, row, col):
        if (row < 0 or row >= ROWS) \
           or (col < 0 or col >= COLS):
            return False
        return not self.grid[row][col]

    def insert(self, form, row, col):
        new_grid = [[self.grid[row][col] for col in range(COLS)]
                    for row in range(ROWS)]
        for tile in form:
            if not self.can_insert(row + tile[0], col + tile[1]):
                return False
            new_grid[row + tile[0]][col + tile[1]] = True
        new_board = Board()
        new_board.grid = tuple(tuple(new_grid[row][col] for col in range(COLS))
                               for row in range(ROWS))
        return new_board

    def match_misses(self, misses):
        for miss in misses:
            if self.grid[miss[0]][miss[1]]:
                return False
        return True
    
    def match_hits(self, hits):
        for hit in hits:
            if not self.grid[hit[0]][hit[1]]:
                return False
        return True

    def print_board(self):
        print(BORDER)
        for row in range(ROWS):
            row_str = ['X' if self.grid[row][col] else '.' for col in range(COLS)]
            print("  " + ''.join(row_str))
        print(BORDER)
        print()

########

class Boards:
    COUNTER = 0
    CHECKPOINTS = (1e5, 5e5, 1e6, 2e6, 5e6, 1e7)
    
    @classmethod
    def generate(cls, board, shapes, hits, misses):
        if not shapes:
            #Boards.COUNTER += 1
            #if Boards.COUNTER in Boards.CHECKPOINTS:
            #    print(f"  Currently at {Boards.COUNTER} boards.")
            if board.match_hits(hits):
                return [board]
            return []

        boards = []
        forms = shapes[0].forms
        remain = shapes[1:]
        for form in forms:
            for row in range(ROWS):
                for col in range(COLS):
                    new_board = board.insert(form, row, col)
                    if new_board and new_board.match_misses(misses):
                        boards.extend(cls.generate(new_board, remain, hits, misses))
        return boards

    def __init__(self, shapes, hits, misses):
        self.boards = Boards.generate(Board(), shapes, hits, misses)
        self.hits = hits
        self.misses = misses
        self.copies = sum(shape.skins for shape in shapes)

    def get_counts(self):
        counts = [[0 for col in range(COLS)]
                  for row in range(ROWS)]

        for board in self.boards:
            for row in range(ROWS):
                for col in range(COLS):
                    if board.grid[row][col]:
                        counts[row][col] += 1
        return counts

    def best_move(self, counts):
        total = len(self.boards)
        if total == 0:
            return NO_BOARDS
        if total == 1:
            return ONE_BOARD
        
        # for a binary outcome, entropy is maxed at p = 1/2
        best = abs(counts[0][0] * 2 - total)
        move = (0, 0)
        for row in range(ROWS):
            for col in range(COLS):
                delta = abs(counts[row][col] * 2 - total)
                if delta == 0:
                    return (row, col)
                elif delta < best:
                    best = delta
                    move = (row, col)
        return move

    def print_state(self):
        states = [["." for col in range(COLS)]
                 for row in range(ROWS)]
        for hit in self.hits:
            states[hit[0]][hit[1]] = "1"
        for miss in self.misses:
            states[miss[0]][miss[1]] = "0"
            
        print(BORDER)
        for state in states:
            print("  " + ''.join(state))
        print(BORDER)
        print(f"Possible boards: {len(self.boards)}" +\
              f" [{len(self.boards) * self.copies}]")
        print(f"Roughly {round(math.log(len(self.boards), 2))} more steps" +\
              " for full information.\n")

    def already_hitmiss(self, tile):
        return tile in self.hits or tile in self.misses

    def add_hit(self, tile):
        if self.already_hitmiss(tile):
            return False
        self.hits.append(tile)
        self.boards = [board for board in self.boards
                       if board.match_hits([tile])]
        return True

    def add_miss(self, tile):
        if self.already_hitmiss(tile):
            return False
        self.misses.append(tile)
        self.boards = [board for board in self.boards
                       if board.match_misses([tile])]
        return True
