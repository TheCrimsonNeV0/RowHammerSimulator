# Memory access time: 50 ns - 100 ns
# Latency when refreshing a row: 5 ns - 10 ns
# TRR lookup: 2 ns - 5 ns
# PARA probability calculation: 1 ns - 2 ns

SIMULATION_SCALE = 0.2  # This value indicates the scale depending on how long the simulation will run
# As the value gets closer to 1, the results will be more realistic

ITERATION_LIMIT = 60 * 5  # How many seconds the simulation should run for

BLAST_RADIUS_RANGE = 2  # This range includes the adjacent row as well
EXPONENTIAL_DECAY_LAMBDA = 0.34

MEMORY_SIZE = 10

# Should be a random value between 150,000 - 200,000
FLIP_THRESHOLD_FIRST = 10000 * SIMULATION_SCALE  # Hammulator configuration
FLIP_THRESHOLD_LAST = 100000 * SIMULATION_SCALE  # Aggressive upper bound for quicker occurrence

TRR_ENABLED = False
TRR_THRESHOLD = 8000 * SIMULATION_SCALE  # Hammulator configuration
TRR_RANGE = 1

PARA_ENABLED = False
PARA_PROBABILITY = 0.001 / SIMULATION_SCALE  # Hammulator configuration
PARA_RANGE = 1

# Custom configuration
ARAR_ENABLED = False
ARAR_CHECK_FROM_LOOKUP = True
ARAR_FREQUENCY = 20
ARAR_RANGE = 2
ARAR_PROBABILITY_START = 0.00001 / SIMULATION_SCALE
ARAR_PROBABILITY_END = 0.001 / SIMULATION_SCALE
ARAR_PROBABILITY_AVERAGE = (ARAR_PROBABILITY_START + ARAR_PROBABILITY_END) / 2
ARAR_ADAPTATION_RATE = 0.0001 / SIMULATION_SCALE
