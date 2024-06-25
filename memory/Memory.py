import copy
import math
import random

import Configurations
from enumerations import Enumerations
import OperationTimes
from memory.MemoryCell import MemoryCell
from utility import Utility


class Memory:
    def __init__(self, size=Configurations.MEMORY_SIZE,
                 blast_radius_range=Configurations.BLAST_RADIUS_RANGE,
                 flip_threshold_first=Configurations.FLIP_THRESHOLD_FIRST,
                 flip_threshold_last=Configurations.FLIP_THRESHOLD_LAST,
                 trr_enabled=Configurations.TRR_ENABLED,
                 trr_threshold=Configurations.TRR_THRESHOLD,
                 para_enabled=Configurations.PARA_ENABLED,
                 para_probability=Configurations.PARA_PROBABILITY,
                 arar_enabled=Configurations.ARAR_ENABLED,
                 arar_check_from_lookup=Configurations.ARAR_CHECK_FROM_LOOKUP,
                 arar_range=Configurations.ARAR_RANGE):
        self.size = size
        self.blast_radius_range = blast_radius_range
        self.flip_threshold_first = flip_threshold_first
        self.flip_threshold_last = flip_threshold_last
        self.trr_enabled = trr_enabled
        self.trr_threshold = trr_threshold
        self.para_enabled = para_enabled
        self.para_probability = para_probability
        self.arar_enabled = arar_enabled
        self.arar_check_from_lookup = arar_check_from_lookup
        self.arar_range = arar_range

        self.access_count = 0
        self.time_in_ns = 0
        self.trr_refresh_count = 0
        self.para_row_activation_count = 0
        self.arar_row_activation_count = 0

        self.arar_probability_cached = Configurations.ARAR_PROBABILITY_START

        self.memory = []
        self.memory_snapshot = []
        for i in range(size):
            self.memory.append(MemoryCell())

        self.trr_access_count_lookup = []
        for i in range(size):
            self.trr_access_count_lookup.append(0)

        self.arar_access_count_lookup = []
        self.arar_refresh_count_lookup = []
        self.arar_current_probabilities = []
        for i in range(size):
            self.arar_access_count_lookup.append(0)
            self.arar_refresh_count_lookup.append(0)
            self.arar_current_probabilities.append(Configurations.ARAR_PROBABILITY_START)

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
        self.access_count += 1

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
            for i in range(2):
                if 0 <= row - i or row + i < self.size:
                    self.increment_time(Enumerations.PARA_CHECK_PROBABILITY)

        # Adaptive Row Activation and Refresh
        if self.arar_enabled:
            #  Update probabilities in the lookup table once every frequency
            if self.access_count % math.ceil(Configurations.ARAR_FREQUENCY) == 0:
                self.adaptive_row_activation_and_refresh_update(row)
                # TODO: Add delay of calculation (division) and use a loop to calculate for each iteration
                self.increment_time(Enumerations.ARAR_CALCULATE_PROBABILITY)  # Mathematical calculation delay

            #  Depending on the configuration, execute necessary instance
            if self.arar_check_from_lookup:
                self.adaptive_row_activation_and_refresh_check_from_lookup(row)
                self.increment_time(Enumerations.ARAR_LOOKUP)  # Same with TRR, reads and writes to lookup table
                self.increment_time(Enumerations.ARAR_CHECK_PROBABILITY)  # Same with PARA, checks should refresh
            else:
                self.adaptive_row_activation_and_refresh_check_from_cache(row)
                self.increment_time(Enumerations.ARAR_CHECK_PROBABILITY)

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

    #  CUSTOM OPERATIONS BEGIN

    def adaptive_row_activation_and_refresh_update(self, row):  # Experimental Mitigation Method
        if row == 0:
            adjusted_probability_next = Utility.gradient_ascent(self.arar_current_probabilities[row + 1])
            self.arar_current_probabilities[row + 1] = adjusted_probability_next
            for i in range(2, self.blast_radius_range + 1):
                if row + i < self.size:
                    self.arar_current_probabilities[row + i] = adjusted_probability_next / i
            if self.arar_probability_cached < self.arar_current_probabilities[row + 1]:
                self.arar_probability_cached = self.arar_current_probabilities[row + 1]
        elif row == self.size - 1:
            adjusted_probability_previous = Utility.gradient_ascent(self.arar_current_probabilities[row - 1])
            self.arar_current_probabilities[row - 1] = adjusted_probability_previous
            for i in range(2, self.blast_radius_range + 1):
                if 0 <= row - i:
                        self.arar_current_probabilities[row - i] = adjusted_probability_previous / i
            if self.arar_probability_cached < self.arar_current_probabilities[row - 1]:
                self.arar_probability_cached = self.arar_current_probabilities[row - 1]
        else:
            adjusted_probability_next = Utility.gradient_ascent(self.arar_current_probabilities[row + 1])
            adjusted_probability_previous = Utility.gradient_ascent(self.arar_current_probabilities[row - 1])

            self.arar_current_probabilities[row + 1] = adjusted_probability_next
            self.arar_current_probabilities[row - 1] = adjusted_probability_previous
            for i in range(2, self.blast_radius_range + 1):
                if row + i < self.size:
                    self.arar_current_probabilities[row + i] = adjusted_probability_next / i
                if 0 <= row - i:
                    self.arar_current_probabilities[row - i] = adjusted_probability_previous / i

            higher_probability = max(self.arar_current_probabilities[row + 1], self.arar_current_probabilities[row - 1])
            if self.arar_probability_cached < higher_probability:
                self.arar_probability_cached = higher_probability

    def adaptive_row_activation_and_refresh_check_from_lookup(self, row):
        for i in range(1, self.blast_radius_range + 1):
            if row + i < self.size:
                random_value = random.random()
                if random_value <= self.arar_current_probabilities[row + i]:
                    self.refresh_row(row + i)
                    self.arar_current_probabilities[row + i] = Configurations.ARAR_PROBABILITY_START
                    self.arar_row_activation_count += 1
                    self.log_output(row + i, Enumerations.ARAR_ROW_ACTIVATION)

            if 0 <= row - i:
                random_value = random.random()
                if random_value <= self.arar_current_probabilities[row - i]:
                    self.refresh_row(row - i)
                    self.arar_current_probabilities[row - i] = Configurations.ARAR_PROBABILITY_START
                    self.arar_row_activation_count += 1
                    self.log_output(row - i, Enumerations.ARAR_ROW_ACTIVATION)

    def adaptive_row_activation_and_refresh_check_from_cache(self, row):
        for i in range(1, self.arar_range + 1):
            if row + i < self.size:
                random_value = random.random()
                if random_value <= self.arar_probability_cached:
                    self.refresh_row(row + i)
                    self.arar_current_probabilities[row + i] = Configurations.ARAR_PROBABILITY_START
                    self.arar_row_activation_count += 1
                    self.log_output(row + i, Enumerations.ARAR_ROW_ACTIVATION)

            if 0 <= row - i:
                random_value = random.random()
                if random_value <= self.arar_probability_cached:
                    self.refresh_row(row - i)
                    self.arar_current_probabilities[row - i] = Configurations.ARAR_PROBABILITY_START
                    self.arar_row_activation_count += 1
                    self.log_output(row - i, Enumerations.ARAR_ROW_ACTIVATION)

    def adaptive_row_activation_and_refresh_check_static(self):  # Not used in the current implementation
        for i in range(len(self.memory)):
            random_value = random.random()
            if random_value <= Configurations.ARAR_PROBABILITY_AVERAGE:
                self.refresh_row(i)
                self.arar_current_probabilities[i] = Configurations.ARAR_PROBABILITY_START
                self.arar_row_activation_count += 1
                self.log_output(i, Enumerations.ARAR_ROW_ACTIVATION)

    #  CUSTOM OPERATIONS END

    def should_flip_probabilistic(self, row):
        # This section uses the calculation logic proposed in Hammulator

        adjacent_access_count = self.get_adjacent_access_count_for_refresh(row)
        random_value = random.random()
        probability_threshold = (adjacent_access_count - self.flip_threshold_first) / (
                    self.flip_threshold_last - self.flip_threshold_first)

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
            adjacent_access_count += left_blast_radius_impacts[i] * Utility.exponential_decay(i + 2)  # +2 for distance

        for i in range(0, len(right_blast_radius_impacts)):
            a = adjacent_access_count
            adjacent_access_count += right_blast_radius_impacts[i] * Utility.exponential_decay(i + 2)  # +2 for distance

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
            self.time_in_ns += random.randint(OperationTimes.PARA_PROBABILITY_CHECK_LOW,
                                              OperationTimes.PARA_PROBABILITY_CHECK_HIGH)
        elif operation == Enumerations.ARAR_LOOKUP:
            self.time_in_ns += random.randint(OperationTimes.ARAR_LOOKUP_LOW, OperationTimes.ARAR_LOOKUP_HIGH)
        elif operation == Enumerations.ARAR_CHECK_PROBABILITY:
            self.time_in_ns += random.randint(OperationTimes.ARAR_PROBABILITY_CHECK_LOW,
                                              OperationTimes.ARAR_PROBABILITY_CHECK_HIGH)
        elif operation == Enumerations.ARAR_CALCULATE_PROBABILITY:
            self.time_in_ns += random.randint(OperationTimes.ARAR_CALCULATE_PROBABILITY_LOW,
                                              OperationTimes.ARAR_CALCULATE_PROBABILITY_HIGH)

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

        # Custom operations
        elif operation == Enumerations.ARAR_ROW_ACTIVATION:
            print('Adaptive Row Activation and Refresh: ' + str(row))

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