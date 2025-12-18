# Symmetries
# 8 - 0 refl & 4/4 rot (e.g. CANE)
# 4 - 0 refl & 2/4 rot (e.g. SCARF)
# 2 - 0 refl & 1/4 rot (e.g. ?pinwheel?)
# 4 - 1 refl & 4/4 rot (e.g. TREE)
## ? - 1 refl & 2/4 rot
## ? - 1 refl & 1/4 rot
## ? - 2 refl & 4/4 rot
# 2 - 2 refl & 2/4 rot (e.g. GIFT)
# 1 - 2 refl & 1/4 rot (e.g. STAR)

# MH definitely rotates all shapes
# MH definitely reflects the non-reflexive shapes
# Case 1: MH reflects asymmetrical shapes - 8/4 forms per shape
# Case 2: MH reflects all shapes - 8 forms per shape

class Shape:
    def __init__(self, refl, rot, *tiles):
        rots = [tiles]
        for i in range(1, rot):
            tiles = tuple((-tile[1], tile[0]) for tile in tiles)
            rots.append(tiles)

        refls = []
        if refl:
            for shape in rots:
                refls.append(tuple((-tile[0], tile[1]) for tile in shape))

        self.forms = tuple(rots + refls)
        self.skins = 4 // rot

    def print_shape(self):
        form_0 = self.forms[0][0]
        pass
        #TODO

########
#NAME   = Shape(will be refl?, num of rotations,
#               *extremes,
#               *rest)

CANE    = Shape(True, 4,
                (0,1), (3,0),
                (1,1), (2,1), (3,1), (2,0))
CANDLE  = Shape(False, 4,
                (0,0), (1,2), (2,0),
                (1,0), (1,1))
COOKIE  = Shape(False, 4,
                (0,0), (1,2),
                (1,0), (0,1), (0,2))
GIFT4   = Shape(False, 1,
                (0,0), (1,1),
                (0,1), (1,0))
GIFT6   = Shape(False, 2,
                (0,0), (1,2),
                (0,2), (1,0), (0,1), (1,1))
HAT     = Shape(False, 4,
                (0,0), (2,2), (3,0),
                (1,2), (2,0), (1,0), (1,1), (2,1))
LOG     = Shape(False, 2,
                (0,0), (4,0),
                (1,0), (2,0), (3,0))
SCARF   = Shape(True, 2,
                (0,0), (2,1),
                (1,0), (1,1))
STAR    = Shape(False, 1,
                (0,1), (2,1),
                (1,2), (1,0), (1,1))
TREE    = Shape(False, 4,
                (0,0), (1,2), (2,0),
                (0,1), (2,1), (1,0), (1,1))
WREATH  = Shape(False, 1,
                (0,0), (2,2), (0,2), (2,0),
                (0,1), (1,2), (2,1), (1,0))
