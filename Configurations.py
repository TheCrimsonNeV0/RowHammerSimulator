# Memory access time: 50 ns - 100 ns
# Latency when refreshing a row: 5 ns - 10 ns
# TRR lookup: 2 ns - 5 ns
# PARA probability calculation: 1 ns - 2 ns

MEMORY_SIZE = 10

# Should be a random value between 150,000 - 200,000
FLIP_THRESHOLD_FIRST = 1500
FLIP_THRESHOLD_LAST = 2000

TRR_ENABLED = False
TRR_THRESHOLD = 1000  # 1/2 - 1/4 of the flip threshold

PARA_ENABLED = False
PARA_PROBABILITY = 0.005