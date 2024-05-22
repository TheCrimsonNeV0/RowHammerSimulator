import copy
import random

import Configurations
from enumarations import Enumarations, OperationTimes
from memory.MemoryCell import MemoryCell


class Memory:
    memory = []
    memory_snapshot = []
    trr_access_count_lookup = []

    time_in_ns = 0

    def __init__(self, size=Configurations.MEMORY_SIZE,
                 flip_threshold_first=Configurations.FLIP_THRESHOLD_FIRST,
                 flip_threshold_last=Configurations.FLIP_THRESHOLD_LAST,
                 trr_enabled=Configurations.TRR_ENABLED,
                 trr_threshold=Configurations.TRR_THRESHOLD,
                 para_enabled=Configurations.PARA_ENABLED,
                 para_probability=Configurations.PARA_PROBABILITY):
        self.size = size
        self.flip_threshold_first = flip_threshold_first
        self.flip_threshold_last = flip_threshold_last
        self.trr_enabled = trr_enabled
        self.trr_threshold = trr_threshold
        self.para_enabled = para_enabled
        self.para_probability = para_probability

        self.memory = []
        for i in range(size):
            self.memory.append(MemoryCell(0))
            self.memory_snapshot.append(MemoryCell(0))

        self.trr_access_count_lookup = []
        for i in range(size):
            self.trr_access_count_lookup.append(0)

    def get_access_count(self, row):
        return self.memory[row].access_count

    def get_memory(self):
        return self.memory

    def get_memory_copy(self):
        return copy.deepcopy(self.memory)

    def get_memory_size(self):
        return len(self.size)

    def take_snapshot(self):
        for row in range(len(self.memory)):
            self.memory_snapshot[row] = self.memory[row]

    def load_snapshot(self):
        for row in range(len(self.memory)):
            self.memory[row].did_flip = self.memory_snapshot[row].did_flip

    def access(self, row):
        self.memory[row].access()

        if row == 0:
            self.memory[row + 1].left_access_count += 1
        elif row == self.size - 1:
            self.memory[row - 1].right_access_count += 1
        else:
            self.memory[row + 1].left_access_count += 1
            self.memory[row - 1].right_access_count += 1

            self.increment_time(Enumarations.MEMORY_ACCESS)

        # Simulation operations
        if row == 0:
            if self.flip_threshold_first <= self.get_adjacent_access_count(row + 1) and not self.memory[row + 1].did_flip:
                if self.should_flip_probabilistic(row + 1):
                    self.memory[row + 1].flip()
                    self.memory[row + 1].left_access_count = 0
                    self.memory[row + 1].right_access_count = 0
        elif row == self.size - 1:
            if self.flip_threshold_first <= self.get_adjacent_access_count(row - 1) and not self.memory[row - 1].did_flip:
                if self.should_flip_probabilistic(row - 1):
                    self.memory[row - 1].flip()
                    self.memory[row - 1].left_access_count = 0
                    self.memory[row - 1].right_access_count = 0
        else:
            if self.flip_threshold_first <= self.get_adjacent_access_count(row + 1) and not self.memory[row + 1].did_flip:
                if self.should_flip_probabilistic(row + 1):
                    self.memory[row + 1].flip()
                    self.memory[row + 1].left_access_count = 0
                    self.memory[row + 1].right_access_count = 0
            if self.flip_threshold_first <= self.get_adjacent_access_count(row - 1) and not self.memory[row - 1].did_flip:
                if self.should_flip_probabilistic(row - 1):
                    self.memory[row - 1].flip()
                    self.memory[row - 1].left_access_count = 0
                    self.memory[row - 1].right_access_count = 0

        # Mitigation operations
        # Target Row Refresh
        if self.trr_enabled:
            self.target_row_refresh(row)
            self.increment_time(Enumarations.TRR_LOOKUP)

        # Probabilistic Adjacent Row Activation
        if self.para_enabled:
            self.probabilistic_adjacent_row_activation(row)
            self.increment_time(Enumarations.PARA_CHECK_PROBABILITY)

    def target_row_refresh(self, row):
        self.increment_trr_lookup(row)
        if row == 0:
            if self.trr_threshold <= self.trr_access_count_lookup[row + 1]:
                self.trr_access_count_lookup[row + 1] = 0
                self.refresh_row(row + 1)
                self.log_output(row + 1, Enumarations.TRR_REFRESH)
        elif row == self.size - 1:
            if self.trr_threshold <= self.trr_access_count_lookup[row - 1]:
                self.trr_access_count_lookup[row - 1] = 0
                self.refresh_row(row - 1)
                self.log_output(row - 1, Enumarations.TRR_REFRESH)
        else:
            if self.trr_threshold <= self.trr_access_count_lookup[row + 1]:
                self.trr_access_count_lookup[row + 1] = 0
                self.refresh_row(row + 1)
                self.log_output(row + 1, Enumarations.TRR_REFRESH)

            if self.trr_threshold <= self.trr_access_count_lookup[row - 1]:
                self.trr_access_count_lookup[row - 1] = 0
                self.refresh_row(row - 1)
                self.log_output(row - 1, Enumarations.TRR_REFRESH)

    def probabilistic_adjacent_row_activation(self, row):
        random_value = random.random()
        if random_value <= self.para_probability:
            if row == 0:
                self.refresh_row(row + 1)
            elif row == self.size - 1:
                self.refresh_row(row - 1)
            else:
                self.refresh_row(row + 1)
                self.refresh_row(row - 1)

        if random.random() <= self.para_probability:
            self.refresh_row(row)
            self.log_output(row, Enumarations.PARA_ROW_ACTIVATION)

    def should_flip_probabilistic(self, row):
        # This section uses the calculation function proposed in Hammulator

        adjacent_access_count = self.get_adjacent_access_count(row)
        random_value = random.random()
        probability_threshold = (adjacent_access_count - self.flip_threshold_first) / (self.flip_threshold_last - self.flip_threshold_first)

        if random_value <= probability_threshold:
            return True
        else:
            return False

    def flip(self, row):
        self.memory[row].flip()
        self.log_output(row, Enumarations.BIT_FLIP)

    def refresh_row(self, row):
        self.memory[row].did_flip = False
        self.increment_time(Enumarations.MEMORY_ACCESS)

    def refresh_row_from_snapshot(self, row):  # Returns True if the refresh was successful
        refreshed = self.memory[row].did_flip != self.memory_snapshot[row].did_flip
        self.memory[row].did_flip = self.memory_snapshot[row].did_flip
        return refreshed

    def get_adjacent_access_count(self, row):
        return self.memory[row].left_access_count + self.memory[row].right_access_count

    def reset_adjacent_access_count(self, row):
        if row == 0:
            self.memory[row + 1].left_access_count = 0
        elif row == self.size - 1:
            self.memory[row - 1].right_access_count = 0
        else:
            self.memory[row + 1].left_access_count = 0
            self.memory[row - 1].right_access_count = 0

    def increment_trr_lookup(self, row):
        if row == 0:
            self.trr_access_count_lookup[row + 1] += 1
        elif row == self.size - 1:
            self.trr_access_count_lookup[row - 1] += 1
        else:
            self.trr_access_count_lookup[row + 1] += 1
            self.trr_access_count_lookup[row - 1] += 1

    def increment_time(self, operation):
        if operation == Enumarations.MEMORY_ACCESS:
            self.time_in_ns += random.randint(OperationTimes.MEMORY_ACCESS_LOW, OperationTimes.MEMORY_ACCESS_HIGH)
        elif operation == Enumarations.REFRESH:
            self.time_in_ns += random.randint(OperationTimes.REFRESH_LOW, OperationTimes.REFRESH_HIGH)
        elif operation == Enumarations.TRR_LOOKUP:
            self.time_in_ns += random.randint(OperationTimes.TRR_LOOKUP_LOW, OperationTimes.TRR_LOOKUP_HIGH)
        elif operation == Enumarations.PARA_CHECK_PROBABILITY:
            self.time_in_ns += random.randint(OperationTimes.PARA_PROBABILITY_CHECK_LOW, OperationTimes.PARA_PROBABILITY_CHECK_HIGH)

    def log_output(self, row, operation):
        if operation == Enumarations.MEMORY_ACCESS:
            print('Memory access: ' + str(row))
        elif operation == Enumarations.BIT_FLIP:
            print('Bit flip: ' + str(row + 1))
        elif operation == Enumarations.REFRESH:
            print('Refresh: ' + str(row))
        elif operation == Enumarations.TRR_REFRESH:
            print('Target Row Refresh: ' + str(row))
        elif operation == Enumarations.PARA_ROW_ACTIVATION:
            print('Probabilistic Adjacent Row Activation: ' + str(row))

