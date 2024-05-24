# Memory access time: 50 ns - 100 ns
# Latency when refreshing a row: 5 ns - 10 ns
# TRR lookup: 2 ns - 5 ns
# PARA probability calculation: 1 ns - 2 ns

MEMORY_SIZE = 10

# Should be a random value between 150,000 - 200,000
FLIP_THRESHOLD_FIRST = 10000  # Hammulator configuration
FLIP_THRESHOLD_LAST = 100000  # Aggressive upper bound for quicker occurance

TRR_ENABLED = False
TRR_THRESHOLD = 8000  # Hammulator configuration

PARA_ENABLED = False
PARA_PROBABILITY = 0.001  # Hammulator configuration

# Custom configurations
ARAR_PROBABILITY_LOW = 0.0001
ARAR_PROBABILITY_HIGH = 1.0