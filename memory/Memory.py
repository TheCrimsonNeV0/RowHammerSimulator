import copy
import random

import Configurations
from memory.MemoryCell import MemoryCell


class Memory:
    __memory__ = []
    __memory_snapshot__ = []
    __trr_access_count_lookup__ = []

    time_in_ns = 0

    def __init__(self, size=Configurations.MEMORY_SIZE, flip_threshold=Configurations.FLIP_THRESHOLD,
                 trr_enabled=Configurations.TRR_ENABLED, trr_threshold=Configurations.TRR_THRESHOLD,
                 para_enabled=Configurations.PARA_ENABLED, para_probability=Configurations.PARA_PROBABILITY):
        self.__size__ = size
        self.__flip_threshold__ = flip_threshold
        self.trr_enabled = trr_enabled
        self.__trr_threshold__ = trr_threshold
        self.para_enabled = para_enabled
        self.__para_probability__ = para_probability

        self.__memory__ = []
        for i in range(size):
            self.__memory__.append(MemoryCell(0))
            self.__memory_snapshot__.append(MemoryCell(0))

        self.__trr_access_count_lookup__ = []
        for i in range(size):
            self.__trr_access_count_lookup__.append(0)

    def get_access_count(self, row):
        return self.__memory__[row].access_count

    def get_memory(self):
        return self.__memory__

    def get_memory_copy(self):
        return copy.deepcopy(self.__memory__)

    def get_memory_size(self):
        return len(self.__size__)

    def take_snapshot(self):
        for row in range(len(self.__memory__)):
            self.__memory_snapshot__[row] = self.__memory__[row]

    def load_snapshot(self):
        for row in range(len(self.__memory__)):
            self.__memory__[row].did_flip = self.__memory_snapshot__[row].did_flip

    def access(self, row):
        self.__memory__[row].access()

        if row == 0:
            self.__memory__[row + 1].left_access_count += 1
        elif row == self.__size__ - 1:
            self.__memory__[row - 1].right_access_count += 1
        else:
            self.__memory__[row + 1].left_access_count += 1
            self.__memory__[row - 1].right_access_count += 1

            self.time_in_ns += random.randint(50, 100)  # Access time

        # Simulation operations
        if row == 0:
            if self.__flip_threshold__ <= self.__memory__[row + 1].left_access_count + self.__memory__[row + 1].right_access_count and not self.__memory__[row + 1].did_flip:
                self.__memory__[row + 1].flip()
                self.__memory__[row + 1].left_access_count = 0
                self.__memory__[row + 1].right_access_count = 0
        elif row == self.__size__ - 1:
            if self.__flip_threshold__ <= self.__memory__[row - 1].left_access_count + self.__memory__[row - 1].right_access_count and not self.__memory__[row - 1].did_flip:
                self.__memory__[row - 1].flip()
                self.__memory__[row - 1].left_access_count = 0
                self.__memory__[row - 1].right_access_count = 0
        else:
            if self.__flip_threshold__ <= self.__memory__[row + 1].left_access_count + self.__memory__[row + 1].right_access_count and not self.__memory__[row + 1].did_flip:
                self.__memory__[row + 1].flip()
                self.__memory__[row + 1].left_access_count = 0
                self.__memory__[row + 1].right_access_count = 0

            if self.__flip_threshold__ <= self.__memory__[row - 1].left_access_count + self.__memory__[
                row - 1].right_access_count and not self.__memory__[row - 1].did_flip:
                self.__memory__[row - 1].flip()
                self.__memory__[row - 1].left_access_count = 0
                self.__memory__[row - 1].right_access_count = 0

        # Mitigation operations
        # Target Row Refresh
        if self.trr_enabled:
            self.target_row_refresh(row)
            self.time_in_ns += random.randint(2, 5)  # TRR Lookup

        # Probabilistic Adjacent Row Activation
        if self.para_enabled:
            self.probabilistic_adjacent_row_activation(row)
            self.time_in_ns += random.randint(1, 2)  # PARA Probability

    def target_row_refresh(self, row):
        self.increment_trr_lookup(row)
        if row == 0:
            if self.__trr_threshold__ <= self.__trr_access_count_lookup__[row + 1]:
                self.__trr_access_count_lookup__[row + 1] = 0
                self.refresh_row(row + 1)
                print("Target Row Refresh on row", row + 1)
        elif row == self.__size__ - 1:
            if self.__trr_threshold__ <= self.__trr_access_count_lookup__[row - 1]:
                self.__trr_access_count_lookup__[row - 1] = 0
                self.refresh_row(row - 1)
                print("Target Row Refresh on row", row - 1)
        else:
            if self.__trr_threshold__ <= self.__trr_access_count_lookup__[row + 1]:
                self.__trr_access_count_lookup__[row + 1] = 0
                self.refresh_row(row + 1)
                print("Target Row Refresh on row", row + 1)

            if self.__trr_threshold__ <= self.__trr_access_count_lookup__[row - 1]:
                self.__trr_access_count_lookup__[row - 1] = 0
                self.refresh_row(row - 1)
                print("Target Row Refresh on row", row - 1)

    def probabilistic_adjacent_row_activation(self, row):
        if random.random() <= self.__para_probability__:
            self.refresh_row(row)
            print("Probabilistic Adjacent Row Activation on ", row)

    def flip(self, row):
        self.__memory__[row].flip()

    def refresh(self):
        for row in self.__memory__:
            row.did_flip = False

    def refresh_row(self, row):
        self.__memory__[row].did_flip = False
        self.time_in_ns += random.randint(5, 10)

    def refresh_row_from_snapshot(self, row):  # Returns True if the refresh was successful
        refreshed = self.__memory__[row].did_flip != self.__memory_snapshot__[row].did_flip
        self.__memory__[row].did_flip = self.__memory_snapshot__[row].did_flip
        return refreshed

    def get_adjacent_access_count(self, row):
        adjacent_access_count = 0
        if row == 0:
            adjacent_access_count = self.__memory__[row + 1].left_access_count
        elif row == self.__size__ - 1:
            adjacent_access_count = self.__memory__[row - 1].right_access_count
        else:
            adjacent_access_count = (self.__memory__[row + 1].left_access_count
                                     + self.__memory__[row - 1].right_access_count)
        return adjacent_access_count

    def reset_adjacent_access_count(self, row):
        if row == 0:
            self.__memory__[row + 1].left_access_count = 0
        elif row == self.__size__ - 1:
            self.__memory__[row - 1].right_access_count = 0
        else:
            self.__memory__[row + 1].left_access_count = 0
            self.__memory__[row - 1].right_access_count = 0

    def increment_trr_lookup(self, row):
        if row == 0:
            self.__trr_access_count_lookup__[row + 1] += 1
        elif row == self.__size__ - 1:
            self.__trr_access_count_lookup__[row - 1] += 1
        else:
            self.__trr_access_count_lookup__[row + 1] += 1
            self.__trr_access_count_lookup__[row - 1] += 1
