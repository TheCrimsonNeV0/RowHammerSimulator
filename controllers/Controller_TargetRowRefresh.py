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


class Controller_TargetRowRefresh:
    def __init__(self, writer, stop_event):
        self.memory = Memory(Configurations.MEMORY_SIZE,
                             Configurations.FLIP_THRESHOLD_FIRST,
                             Configurations.FLIP_THRESHOLD_LAST,
                             True, Configurations.TRR_THRESHOLD, False, 0)
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
                self.memory.access(AGGRESSOR_ROW_ONE)
                self.memory.access(AGGRESSOR_ROW_TWO)
            elif operation == 'log':
                print('Time passed (seconds): ' + str(self.iteration_count))

                simulation_time = self.memory.time_in_ns
                adjacent_access_count = self.memory.get_adjacent_access_count(VICTIM_ROW)
                trr_count = self.memory.trr_refresh_count
                flip_count = self.memory.memory[VICTIM_ROW].flip_count

                self.writer.writerow([self.iteration_count, simulation_time, adjacent_access_count, trr_count, flip_count])
                self.iteration_count += 1
            return True


def hammer(controller, stop_event):  # Simulate hammering behavior
    if not stop_event.is_set() and controller.edit_list('hammer'):
        threading.Timer(0.01, hammer, args=(controller, stop_event)).start()


def log(controller, stop_event):
    if not stop_event.is_set() and controller.edit_list('log'):
        threading.Timer(1, log, args=(controller, stop_event)).start()


def main():
    fields = ['real_time', 'simulation_time_ns', 'adjacent_access_count_of_victim', 'trr_count', 'flip_count']
    file = open('../outputs/output_target_row_refresh.csv', 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(fields)

    stop_event = threading.Event()
    controller = Controller_TargetRowRefresh(writer, stop_event)

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
