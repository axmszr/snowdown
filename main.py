from dlu.uiux import *

# Shapes:
#   CANE, CANDLE, COOKIE, GIFT4, GIFT6,
#   HAT, LOG, SCARF, STAR, TREE, WREATH

# First coordinate is row, from top to bottom
# Second coordinate is column, from left to right
# Start from (0,0) in the top-left, then trace an 'L' shape

# e.g.
# Solved:
#  =====================
#  X . . . . X X X . . .
#  X X X . . X . X . . .
#  X . X X . X X X . . .
#  . . X X X . X X . . .
#  . . X X . . X X . . .
#  . . . . . . X X . . .
#  =====================
#
# Current info:
#  =====================
#  . . . . . . 1 1 . . .
#  . 1 1 0 . 1 0 . 0 . .
#  . 0 . . 0 . . . . . .
#  . . . . . . 1 . 0 . .
#  . . . . . 0 . 1 . . .
#  . . . . . . . 1 . . .
#  =====================

########

shapes  = [CANDLE, GIFT6, TREE, WREATH]
hits    = [(1,1), (1,2), (1,5), (3,6), (4,7), (5,7), (0,6), (0,7)]
misses  = [(1,3), (2,1), (1,8), (4,5), (2,4), (1,6), (3,8)]

########

state   = play(shapes, hits, misses, False)

# True  - FAST mode, max's entropy/min's steps til full info
# False - SLOW mode, max's hits/min's misses til full info (generally better)
