# Memory access time: 50 ns - 100 ns
# Latency when refreshing a row: 5 ns - 10 ns
# TRR lookup: 2 ns - 5 ns
# PARA probability calculation: 1 ns - 2 ns

MEMORY_SIZE = 10

BLAST_RADIUS_RANGE = 2  # This range includes the adjacent row as well
                        # Impact starts from 1 and linearly goes to 0

SIMULATION_SCALE = 0.3  # This value indicates the scale depending on how long the simulation will run
                        # As the value gets closer to 1, the results will be more realistic

# Should be a random value between 150,000 - 200,000
FLIP_THRESHOLD_FIRST = 10000 * SIMULATION_SCALE  # Hammulator configuration
FLIP_THRESHOLD_LAST = 100000 * SIMULATION_SCALE  # Aggressive upper bound for quicker occurrence

TRR_ENABLED = False
TRR_THRESHOLD = 8000 * SIMULATION_SCALE  # Hammulator configuration
TRR_RANGE = 2

PARA_ENABLED = False
PARA_PROBABILITY = 0.001 / SIMULATION_SCALE  # Hammulator configuration