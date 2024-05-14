import copy
import random

from memory.MemoryCell import MemoryCell


class Memory:
    __memory__ = []
    __memory_snapshot__ = []
    __trr_access_count_lookup__ = []

    def __init__(self, size, flip_threshold, trr_enabled=False, trr_threshold=0, para_enabled=False, para_probability=0):
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

        # Simulation operations
        if row == 0:
            if self.__flip_threshold__ <= self.get_adjacent_access_count(row + 1) and not self.__memory__[row].did_flip:
                self.__memory__[row + 1].flip()
        elif row == self.__size__ - 1:
            if self.__flip_threshold__ <= self.get_adjacent_access_count(row - 1) and not self.__memory__[row].did_flip:
                self.__memory__[row - 1].flip()
        else:
            if self.__flip_threshold__ <= self.get_adjacent_access_count(row - 1) and not self.__memory__[row].did_flip:
                self.__memory__[row - 1].flip()
            if self.__flip_threshold__ <= self.get_adjacent_access_count(row + 1) and not self.__memory__[row].did_flip:
                self.__memory__[row + 1].flip()

        # Mitigation operations
        # Target Row Refresh
        if self.trr_enabled:
            self.target_row_refresh(row)

        # Probabilistic Adjacent Row Activation
        if self.para_enabled:
            self.probabilistic_adjacent_row_activation(row)

    def target_row_refresh(self, row):
        self.__trr_access_count_lookup__[row] += 1
        if self.__trr_threshold__ <= self.__trr_access_count_lookup__[row]:
            self.refresh_row(row)
            self.__trr_access_count_lookup__[row] = 0
            print("Target Row Refresh on ", row)

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
        self.__memory__[row].refresh()

    def refresh_row_from_snapshot(self, row):  # Returns True if the refresh was successful
        refreshed = self.__memory__[row].did_flip != self.__memory_snapshot__[row].did_flip
        self.__memory__[row].did_flip = self.__memory_snapshot__[row].did_flip
        return refreshed

    def get_adjacent_access_count(self, row):
        adjacent_access_count = 0
        if row == 0:
            adjacent_access_count = self.__memory__[row + 1].get_access_count()
        elif row == self.__size__ - 1:
            adjacent_access_count = self.__memory__[row - 1].get_access_count()
        else:
            adjacent_access_count = (self.__memory__[row - 1].get_access_count()
                                     + self.__memory__[row + 1].get_access_count())
        return adjacent_access_count

