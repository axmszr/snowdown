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

# MH does not seem to do rotations/reflections that do not change shape
# --> no skins
# MH reflects the non-reflexive shapes

def make_shape(refl, rot, *tiles):
    rots = [tiles]
    for i in range(1, rot):
        tiles = tuple((-tile[1], tile[0]) for tile in tiles)
        rots.append(tiles)

    refls = []
    if refl:
        for shape in rots:
            refls.append(tuple((-tile[0], tile[1]) for tile in shape))

    #return (tuple(rots + refls), 4 // rot)
    return tuple(rots + refls)

def print_form(form):
    pass
    #TODO

########
#NAME   = make_shape(chirality, num of rotated forms,
#                    *extremes,
#                    *rest)                             #sketch from (0,0)

CANE    = make_shape(True, 4,
                     (0,1), (3,0),                      ####
                     (1,1), (2,1), (3,1), (2,0))          ##

CANDLE  = make_shape(False, 4,                           #
                     (0,0), (1,2), (2,0),                #
                     (1,0), (1,1))                      ###

COOKIE  = make_shape(False, 4,                          ##
                     (0,0), (1,2),                      #
                     (1,0), (0,1), (0,2))               ##

GIFT4   = make_shape(False, 1,
                     (0,0), (1,1),                      ##
                     (0,1), (1,0))                      ##

GIFT6   = make_shape(False, 2,                          ##
                     (0,0), (1,2),                      ##
                     (0,2), (1,0), (0,1), (1,1))        ##

HAT     = make_shape(False, 4,                           ##
                     (0,0), (2,2), (3,0),                ##
                     (1,2), (2,0), (1,0), (1,1), (2,1)) ####

LOG     = make_shape(False, 2,
                     (0,0), (4,0),
                     (1,0), (2,0), (3,0))               #####

SCARF   = make_shape(True, 2,
                     (0,0), (2,1),                       ##
                     (1,0), (1,1))                      ##

STAR    = make_shape(False, 1,                           #
                     (0,1), (2,1),                      ###
                     (1,2), (1,0), (1,1))                #

TREE    = make_shape(False, 4,                           #
                     (0,0), (1,2), (2,0),               ###
                     (0,1), (2,1), (1,0), (1,1))        ###

WREATH  = make_shape(False, 1,                          ###
                     (0,0), (2,2), (0,2), (2,0),        # #
                     (0,1), (1,2), (2,1), (1,0))        ###
