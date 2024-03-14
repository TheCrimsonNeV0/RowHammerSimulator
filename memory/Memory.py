import copy

from memory.MemoryCell import MemoryCell


class Memory:
    __memory__ = []
    __memory_snapshot__ = []

    def __init__(self, size, flip_threshold):
        self.__size__ = size
        self.__flip_threshold__ = flip_threshold
        self.__memory__ = []
        for i in range(size):
            self.__memory__.append(MemoryCell(0))
            self.__memory_snapshot__.append(MemoryCell(0))

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

