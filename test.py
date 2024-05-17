import random
import numpy as np

# Constants
MEMORY_SIZE = 64 * 1024  # Simulated memory size: 64KB
ROW_SIZE = 256  # Simulated row size: 256 bytes
HAMMER_COUNT = 100000  # Number of accesses to hammer a row

# Initialize memory with zeros
memory = np.zeros(MEMORY_SIZE, dtype=np.uint8)

def hammer_row(memory, row_index, hammer_count):
    start = row_index * ROW_SIZE
    end = start + ROW_SIZE
    for _ in range(hammer_count):
        for i in range(start, end):
            memory[i] = memory[i] ^ 1  # Simulate a memory access and potential bit flip

def check_bit_flips(memory):
    bit_flips = 0
    for i in range(MEMORY_SIZE):
        if memory[i] != 0:
            bit_flips += 1
            print(f"Bit flip detected at byte {i}")
    return bit_flips

def main():
    # Hammer adjacent rows (e.g., rows 1 and 3 to affect row 2)
    hammer_row(memory, 1, HAMMER_COUNT)
    hammer_row(memory, 3, HAMMER_COUNT)

    # Check for bit flips in the victim row (e.g., row 2)
    victim_row_start = 2 * ROW_SIZE
    victim_row_end = victim_row_start + ROW_SIZE
    victim_row_flips = 0

    for i in range(victim_row_start, victim_row_end):
        if memory[i] != 0:
            victim_row_flips += 1
            print(f"Bit flip detected in victim row at byte {i}")

    if victim_row_flips:
        print(f"RowHammer attack simulated: {victim_row_flips} bit flips detected in victim row!")
    else:
        print("No bit flips detected in the victim row.")

if __name__ == "__main__":
    main()
