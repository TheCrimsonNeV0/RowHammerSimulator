#  Documentation:
#  JEDEC Standards
#  Research Papers on RowHammer Mitigations
#  Technical Documentation from DRAM Manufacturers (Micron, Samsung, Hynix...)

#  Timings are given as nanoseconds

MEMORY_ACCESS_LOW = 29  # Without any mitigation method delays
MEMORY_ACCESS_HIGH = 30  # Without any mitigation method delays

REFRESH_LOW = 350  # DDR4 Standard
REFRESH_HIGH = 414  # DDR4 Standard (with 64ns additional delay)

TRR_LOOKUP_LOW = 10
TRR_LOOKUP_HIGH = 20

PARA_PROBABILITY_CHECK_LOW = 1
PARA_PROBABILITY_CHECK_HIGH = 5

ARAR_LOOKUP_LOW = 10
ARAR_LOOKUP_HIGH = 20

ARAR_PROBABILITY_CHECK_LOW = 1
ARAR_PROBABILITY_CHECK_HIGH = 5

ARAR_CALCULATE_PROBABILITY_LOW = 20 # 10 for subtraction, 10 for multiplication
ARAR_CALCULATE_PROBABILITY_HIGH = 40 # 20 for subtraction, 20 for multiplication