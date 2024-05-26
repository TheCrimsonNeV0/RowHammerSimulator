import threading
import time
import csv

import Configurations
from memory.Memory import Memory

file = ''

#  Constant variables
VICTIM_ROW = 4
AGGRESSOR_ROW_ONE = 3
AGGRESSOR_ROW_TWO = 5
ITERATION_LIMIT = 120

PATTERNS = [[1, 3], [3, 5], [5, 7], [7, 9]]


class Controller_NoMitigation:
    def __init__(self, writer, stop_event):
        self.memory = Memory(Configurations.MEMORY_SIZE,
                             Configurations.FLIP_THRESHOLD_FIRST,
                             Configurations.FLIP_THRESHOLD_LAST,
                             False, 0, False, 0)
        self.lock = threading.Lock()
        self.writer = writer
        self.stop_event = stop_event
        self.iteration_count = 0

    def edit_list(self, operation):
        with self.lock:
            if ITERATION_LIMIT <= self.iteration_count:
                self.stop_event.set()
                return False

            if operation == 'hammer_static':
                self.memory.access(AGGRESSOR_ROW_ONE)
                self.memory.access(AGGRESSOR_ROW_TWO)
            elif operation == 'hammer_pattern':
                pattern = PATTERNS[self.iteration_count % len(PATTERNS)]
                self.memory.access(pattern[0])
                self.memory.access(pattern[1])
            elif operation == 'log':
                print('Time passed (seconds): ' + str(self.iteration_count))
                self.memory.print_access_counts()

                simulation_time = self.memory.time_in_ns
                adjacent_access_count = self.memory.get_adjacent_access_count(VICTIM_ROW)
                flip_count = self.memory.memory[VICTIM_ROW].flip_count

                self.writer.writerow([self.iteration_count, simulation_time, adjacent_access_count, flip_count])
                self.iteration_count += 1
            return True


def hammer_static(controller, stop_event):  # Simulate hammering behavior
    if not stop_event.is_set() and controller.edit_list('hammer_static'):
        threading.Timer(0.01, hammer_static, args=(controller, stop_event)).start()

def hammer_pattern(controller, stop_event):  # Simulate hammering behavior
    if not stop_event.is_set() and controller.edit_list('hammer_pattern'):
        threading.Timer(0.01, hammer_pattern, args=(controller, stop_event)).start()

def log(controller, stop_event):
    if not stop_event.is_set() and controller.edit_list('log'):
        threading.Timer(1, log, args=(controller, stop_event)).start()

def main():
    fields = ['real_time', 'simulation_time_ns', 'adjacent_access_count_of_victim', 'flip_count']
    file = open('../outputs/output_no_mitigation.csv', 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(fields)

    stop_event = threading.Event()
    controller = Controller_NoMitigation(writer, stop_event)

    # Create threads
    thread1 = threading.Thread(target=hammer_pattern, args=(controller, stop_event))
    thread2 = threading.Thread(target=log, args=(controller, stop_event))

    # Start both threads
    thread1.start()
    thread2.start()

    try:
        # Keep the main thread alive to allow threads to run
        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping threads...")
    finally:
        file.close()
        # Optionally wait for threads to finish before exiting
        thread1.join()
        thread2.join()


if __name__ == "__main__":
    main()
