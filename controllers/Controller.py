import threading
import time

from memory.Memory import Memory

class Controller:
    def __init__(self):
        self.memory = Memory()
        self.lock = threading.Lock()

    def edit_list(self, editor_name):
        with self.lock:
            if editor_name == 'hammer':
                self.memory.access(3)
                self.memory.access(5)
            elif editor_name == 'log':
                print('Time passed: ' + str(self.memory.time_in_ns), 'ns')
                print('Adjacent access count of victim: ' + str(self.memory.get_adjacent_access_count(4)) + '\n')

def hammer(list_editor):  # Simulate hammering behavior
    list_editor.edit_list('hammer')
    threading.Timer(0.01, hammer, args=(list_editor,)).start()


def log(list_editor):
    list_editor.edit_list('log')
    threading.Timer(2, log, args=(list_editor,)).start()


def main():
    list_editor = Controller()

    # Create threads
    thread1 = threading.Thread(target=hammer, args=(list_editor,))
    thread2 = threading.Thread(target=log, args=(list_editor,))

    # Start both threads
    thread1.start()
    thread2.start()

    try:
        # Keep the main thread alive to allow threads to run
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping threads...")
        # You can add any cleanup logic here
    finally:
        # Optionally wait for threads to finish before exiting
        thread1.join()
        thread2.join()


if __name__ == "__main__":
    main()