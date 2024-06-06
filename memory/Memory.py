import copy
import random

import Configurations
from enumerations import Enumerations
import OperationTimes
from memory.MemoryCell import MemoryCell


class Memory:
    def __init__(self, size=Configurations.MEMORY_SIZE,
                 blast_radius_range=Configurations.BLAST_RADIUS_RANGE,
                 flip_threshold_first=Configurations.FLIP_THRESHOLD_FIRST,
                 flip_threshold_last=Configurations.FLIP_THRESHOLD_LAST,
                 trr_enabled=Configurations.TRR_ENABLED,
                 trr_threshold=Configurations.TRR_THRESHOLD,
                 para_enabled=Configurations.PARA_ENABLED,
                 para_probability=Configurations.PARA_PROBABILITY):
        self.size = size
        self.blast_radius_range = blast_radius_range
        self.flip_threshold_first = flip_threshold_first
        self.flip_threshold_last = flip_threshold_last
        self.trr_enabled = trr_enabled
        self.trr_threshold = trr_threshold
        self.para_enabled = para_enabled
        self.para_probability = para_probability

        self.time_in_ns = 0
        self.trr_refresh_count = 0
        self.para_row_activation_count = 0

        self.memory = []
        self.memory_snapshot = []
        for i in range(size):
            self.memory.append(MemoryCell())

        self.trr_access_count_lookup = []
        for i in range(size):
            self.trr_access_count_lookup.append(0)

        self.arar_access_count_lookup = []
        self.arar_refresh_count_lookup = []
        for i in range(size):
            self.arar_access_count_lookup.append(0)
            self.arar_refresh_count_lookup.append(0)
        self.arar_current_probability = Configurations.ARAR_PROBABILITY_LOW


    def get_access_count(self, row):
        return self.memory[row].access_count

    def get_total_access_count(self):
        total_access_count = 0
        for row in self.memory:
            total_access_count += row.get_access_count()
        return total_access_count

    def get_memory(self):
        return self.memory

    def get_memory_copy(self):
        return copy.deepcopy(self.memory)

    def get_memory_size(self):
        return len(self.size)

    def access(self, row):
        self.memory[row].access()

        if row == 0:
            self.memory[row + 1].increment_left_adjacent_access_count()
        elif row == self.size - 1:
            self.memory[row - 1].increment_right_adjacent_access_count()
        else:
            self.memory[row + 1].increment_left_adjacent_access_count()
            self.memory[row - 1].increment_right_adjacent_access_count()

        for i in range(2, self.blast_radius_range + 1):
            if row + i < self.size:
                self.memory[row + i].increment_left_blast_radius_impact(i - self.blast_radius_range)
            if 0 <= row - i:
                self.memory[row - i].increment_right_blast_radius_impact(i - self.blast_radius_range)

        self.increment_time(Enumerations.MEMORY_ACCESS)

        # Simulation operations
        for i in range(1, self.blast_radius_range + 1):
            if row + i < self.size:
                if self.flip_threshold_first <= self.get_adjacent_access_count_for_refresh(row + i) and not self.memory[row + i].did_flip:
                    if self.should_flip_probabilistic(row + i):
                        self.flip(row + i)
            if 0 <= row - i:
                if self.flip_threshold_first <= self.get_adjacent_access_count_for_refresh(row - i) and not self.memory[row - i].did_flip:
                    if self.should_flip_probabilistic(row - i):
                        self.flip(row - i)

        # Mitigation operations
        # Target Row Refresh
        if self.trr_enabled:
            self.target_row_refresh(row)
            self.increment_time(Enumerations.TRR_LOOKUP)

        # Probabilistic Adjacent Row Activation
        if self.para_enabled:
            self.probabilistic_adjacent_row_activation(row)
            self.increment_time(Enumerations.PARA_CHECK_PROBABILITY)

    def target_row_refresh(self, row):
        self.increment_trr_lookup(row)

        for i in range(1, Configurations.TRR_RANGE + 1):
            if row + i < self.size:
                if self.trr_threshold <= self.trr_access_count_lookup[row + i]:
                    self.trr_access_count_lookup[row + i] = 0
                    self.refresh_row(row + i)
                    self.trr_refresh_count += 1
                    self.log_output(row + i, Enumerations.TRR_REFRESH)

            if 0 <= row - i:
                if self.trr_threshold <= self.trr_access_count_lookup[row - i]:
                    self.trr_access_count_lookup[row - i] = 0
                    self.refresh_row(row - i)
                    self.trr_refresh_count += 1
                    self.log_output(row - i, Enumerations.TRR_REFRESH)

    def probabilistic_adjacent_row_activation(self, row):  # Uses different random values for each adjacent row
        random_value = random.random()

        if row == 0:
            random_value = random.random()
            if random_value <= self.para_probability:
                self.refresh_row(row + 1)
                self.para_row_activation_count += 1
                self.log_output(row + 1, Enumerations.PARA_ROW_ACTIVATION)
        elif row == self.size - 1:
            random_value = random.random()
            if random_value <= self.para_probability:
                self.refresh_row(row - 1)
                self.para_row_activation_count += 1
                self.log_output(row - 1, Enumerations.PARA_ROW_ACTIVATION)
        else:
            random_value_next = random.random()
            random_value_previous = random.random()
            if random_value_next <= self.para_probability:
                self.refresh_row(row + 1)
                self.para_row_activation_count += 1
                self.log_output(row + 1, Enumerations.PARA_ROW_ACTIVATION)
            if random_value_previous <= self.para_probability:
                self.refresh_row(row - 1)
                self.para_row_activation_count += 1
                self.log_output(row - 1, Enumerations.PARA_ROW_ACTIVATION)

    def adaptive_row_activation_and_refresh(self, row):  # Experimental Mitigation Method
        self.increment_arar_lookup(row)

        # TODO: Adapt the refresh probability depending on the access count and refresh count

    def should_flip_probabilistic(self, row):
        # This section uses the calculation logic proposed in Hammulator

        adjacent_access_count = self.get_adjacent_access_count_for_refresh(row)
        random_value = random.random()
        probability_threshold = (adjacent_access_count - self.flip_threshold_first) / (self.flip_threshold_last - self.flip_threshold_first)

        if random_value <= probability_threshold:
            return True
        else:
            return False

    def flip(self, row):
        self.memory[row].flip()
        self.log_output(row, Enumerations.BIT_FLIP)

    def refresh_row(self, row):
        self.memory[row].refresh()
        self.increment_time(Enumerations.MEMORY_ACCESS)

    def get_adjacent_access_count(self, row):
        return self.memory[row].get_adjacent_access_count()

    def get_adjacent_access_count_for_refresh(self, row):
        adjacent_access_count = self.memory[row].left_access_count + self.memory[row].right_access_count
        left_blast_radius_impacts = self.memory[row].get_left_blast_radius_impacts()
        right_blast_radius_impacts = self.memory[row].get_right_blast_radius_impacts()


        for i in range(0, len(left_blast_radius_impacts)):
            a = adjacent_access_count
            adjacent_access_count += (left_blast_radius_impacts[i] * (len(left_blast_radius_impacts) - i) / (len(left_blast_radius_impacts) + 1))

        for i in range(0, len(right_blast_radius_impacts)):
            a = adjacent_access_count
            adjacent_access_count += (right_blast_radius_impacts[i] * (len(right_blast_radius_impacts) - i) / (len(right_blast_radius_impacts) + 1))

        return adjacent_access_count

    def reset_adjacent_access_count(self, row):
        if row == 0:
            self.memory[row + 1].reset_left_adjacent_access_count()
        elif row == self.size - 1:
            self.memory[row - 1].reset_right_adjacent_access_count()
        else:
            self.memory[row + 1].reset_left_adjacent_access_count()
            self.memory[row - 1].reset_right_adjacent_access_count()

    def reset_blast_radius_impact(self, row):
        for i in range(1, Configurations.TRR_RANGE + 1):
            if row + i < self.size:
                self.memory[row + i].reset_blast_radius_impacts()

            if 0 <= row - i:
                self.memory[row - i].reset_blast_radius_impacts()

    def increment_trr_lookup(self, row):
        for i in range(0, Configurations.TRR_RANGE + 1):
            if row + i < self.size:
                self.trr_access_count_lookup[row + i] += 1

            if 0 <= row - i:
                self.trr_access_count_lookup[row - i] += 1

    def increment_arar_lookup(self, row):
        if row == 0:
            self.arar_access_count_lookup[row + 1] += 1
        elif row == self.size - 1:
            self.arar_access_count_lookup[row - 1] += 1
        else:
            self.arar_access_count_lookup[row + 1] += 1
            self.arar_access_count_lookup[row - 1] += 1

    def increment_time(self, operation):
        if operation == Enumerations.MEMORY_ACCESS:
            self.time_in_ns += random.randint(OperationTimes.MEMORY_ACCESS_LOW, OperationTimes.MEMORY_ACCESS_HIGH)
        elif operation == Enumerations.REFRESH:
            self.time_in_ns += random.randint(OperationTimes.REFRESH_LOW, OperationTimes.REFRESH_HIGH)
        elif operation == Enumerations.TRR_LOOKUP:
            self.time_in_ns += random.randint(OperationTimes.TRR_LOOKUP_LOW, OperationTimes.TRR_LOOKUP_HIGH)
        elif operation == Enumerations.PARA_CHECK_PROBABILITY:
            self.time_in_ns += random.randint(OperationTimes.PARA_PROBABILITY_CHECK_LOW, OperationTimes.PARA_PROBABILITY_CHECK_HIGH)

    def log_output(self, row, operation):
        if operation == Enumerations.MEMORY_ACCESS:
            print('Memory access: ' + str(row))
        elif operation == Enumerations.BIT_FLIP:
            print('Bit flip: ' + str(row))
        elif operation == Enumerations.REFRESH:
            print('Refresh: ' + str(row))
        elif operation == Enumerations.TRR_REFRESH:
            print('Target Row Refresh: ' + str(row))
        elif operation == Enumerations.PARA_ROW_ACTIVATION:
            print('Probabilistic Adjacent Row Activation: ' + str(row))

    def print_access_counts(self):
        access_counts = []
        for i in range(self.size):
            access_counts.append(self.memory[i].access_count)
        print(access_counts)

    def print_adjacent_access_counts(self):
        adjacent_access_counts = []
        for i in range(self.size):
            adjacent_access_counts.append(self.memory[i].adjacent_access_count)
        print(adjacent_access_counts)

    def get_flip_count(self):
        flip_count = 0
        for row in self.memory:
            if row.did_flip:
                flip_count += 1
        return flip_count
