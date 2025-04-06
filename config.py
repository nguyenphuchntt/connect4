
#NOTE: RED = 1      |       BLUE = -1       |       NONE = 0
#NOTE: The coordinate origin is located at the top-left.

BOARD_ROWS = 6
BOARD_COLUMNS = 7
ACTION_SIZE = BOARD_COLUMNS

RED_PLAYER = 1      # PLAYER
BLUE_PLAYER = -1    # AI
EMPTY = 0

WINDOW_LENGTH = 4
EXPLORATION_CONST  = 1

N_FILTERS =  128              # Number of convolutional filters used in residual block
N_RES_BLOCKs = 8             # Number of residual blocks used in network
C_PUCT = 2
TEMPERATURE = 1.25
DIRICHLET_ALPHA = 1
DIRICHLET_EPSILON = 0.25
LEANRING_RATE = 0.001
N_SEARCHES = 60

N_ITER = 3
BATCH_SIZE = 64
N_SELFPLAY_ITER = 500
N_EPOCHS = 4


WEIGHT_DECAY = 0.0001


N_PARALLEL = 100