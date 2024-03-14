import threading


# This algorithm should run on a separate thread to simulate the CPU behavior.
def target_row_refresh_instance(memory, target):
    memory_copy = memory.get_memory_copy()
    adjacent_access_count = []
    for row_index in range(memory_copy.get_memory_size()):
        if row_index == 0:
            adjacent_access_count.insert(row_index, memory[row_index].get_access_count())
        elif row_index == memory_copy.get_memory_size() - 1:
            adjacent_access_count.insert(row_index, memory[row_index - 1].get_access_count())
        else:
            adjacent_access_count.insert(row_index, memory[row_index - 1].get_access_count()
                                         + memory[row_index + 1].get_access_count())
    for row_index in range(len(adjacent_access_count)):
        if target <= adjacent_access_count[row_index]:
            memory_copy.refresh_row_from_snapshot(row_index)
    return memory_copy


def probabilistic_adjacent_row_activation_instance(memory, probability):
    memory_copy = memory.get_memory_copy()
    for row_index in range(memory_copy.get_memory_size()):
        random = random.random()
        if random <= probability:
            memory_copy.refresh_row_from_snapshot(row_index)
    return memory_copy
