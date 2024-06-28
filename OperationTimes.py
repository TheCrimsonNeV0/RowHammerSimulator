#  Documentation:
#  JEDEC Standards
#  Research Papers on RowHammer Mitigations
#  Technical Documentation from DRAM Manufacturers (Micron, Samsung, Hynix...)

#  Timings are given as nanoseconds

MEMORY_ACCESS_LOW = 25  # Without any mitigation method delays
MEMORY_ACCESS_HIGH = 35  # Without any mitigation method delays

ADDITION_LOW = 1
ADDITION_HIGH = 3

SUBTRACTION_LOW = 1
SUBTRACTION_HIGH = 3

MULTIPLICATION_LOW = 3
MULTIPLICATION_HIGH = 10

DIVISION_LOW = 10
DIVISION_HIGH = 20

REFRESH_LOW = 350  # DDR4 Standard
REFRESH_HIGH = 385  # DDR4 Standard (with 10% additional delay)

TRR_LOOKUP_LOW = 10
TRR_LOOKUP_HIGH = 20

PARA_PROBABILITY_CHECK_LOW = 1
PARA_PROBABILITY_CHECK_HIGH = 5

ARAR_LOOKUP_LOW = 10
ARAR_LOOKUP_HIGH = 20

ARAR_PROBABILITY_CHECK_LOW = 1
ARAR_PROBABILITY_CHECK_HIGH = 5