# Memory access time: 50 ns - 100 ns
# Latency when refreshing a row: 5 ns - 10 ns
# TRR lookup: 2 ns - 5 ns
# PARA probability calculation: 1 ns - 2 ns

SIMULATION_SCALE = 0.2  # This value indicates the scale depending on how long the simulation will run
# As the value gets closer to 1, the results will be more realistic

BLAST_RADIUS_RANGE = 2  # This range includes the adjacent row as well
# Impact starts from 1 and linearly goes to 0

MEMORY_SIZE = 48

# Should be a random value between 150,000 - 200,000
FLIP_THRESHOLD_FIRST = 10000 * SIMULATION_SCALE  # Hammulator configuration
FLIP_THRESHOLD_LAST = 100000 * SIMULATION_SCALE  # Aggressive upper bound for quicker occurrence

TRR_ENABLED = False
TRR_THRESHOLD = 8000 * SIMULATION_SCALE  # Hammulator configuration
TRR_RANGE = 2

PARA_ENABLED = False
PARA_PROBABILITY = 0.001 / SIMULATION_SCALE  # Hammulator configuration

# Custom configuration
ARAR_ENABLED = False
ARAR_CHECK_FROM_LOOKUP = True
ARAR_FREQUENCY = round(20 * SIMULATION_SCALE)  # Calculation is executed once every ARAR_FREQUENCY iteration
ARAR_RANGE = 2
ARAR_PROBABILITY_START = 0.00001 / SIMULATION_SCALE
ARAR_PROBABILITY_END = 0.001 / SIMULATION_SCALE
ARAR_PROBABILITY_AVERAGE = (ARAR_PROBABILITY_START + ARAR_PROBABILITY_END) / 2
ARAR_ADAPTATION_RATE = 0.0001 / SIMULATION_SCALE
