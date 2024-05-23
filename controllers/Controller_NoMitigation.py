import threading
import time
import csv

import Configurations
from memory.Memory import Memory

file = ''

#  Constant variables
VICTIM_ROW = 4
AGRESSOR_ROW_ONE = 3
AGRESSOR_ROW_TWO = 5
ITERATION_LIMIT = 120


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

            if operation == 'hammer':
                self.memory.access(AGRESSOR_ROW_ONE)
                self.memory.access(AGRESSOR_ROW_TWO)
            elif operation == 'log':
                print('Time passed (seconds): ' + str(self.iteration_count))

                simulation_time = self.memory.time_in_ns
                adjacent_acces_count = self.memory.get_adjacent_access_count(VICTIM_ROW)
                bit_flipped = self.memory.memory[VICTIM_ROW].did_flip

                self.writer.writerow([self.iteration_count, simulation_time, adjacent_acces_count, bit_flipped])
                self.iteration_count += 1
            return True


def hammer(controller, stop_event):  # Simulate hammering behavior
    if not stop_event.is_set() and controller.edit_list('hammer'):
        threading.Timer(0.01, hammer, args=(controller, stop_event)).start()


def log(controller, stop_event):
    if not stop_event.is_set() and controller.edit_list('log'):
        threading.Timer(1, log, args=(controller, stop_event)).start()


def main():
    fields = ['real_time', 'simulation_time_ns', 'adjacent_access_count_of_victim', 'victim_row_bit_flipped']
    file = open('../outputs/output_no_mitigation.csv', 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(fields)

    stop_event = threading.Event()
    controller = Controller_NoMitigation(writer, stop_event)

    # Create threads
    thread1 = threading.Thread(target=hammer, args=(controller, stop_event))
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
