import threading
import time

from memory.Memory import Memory

MEMORY_SIZE = 100
FLIP_THRESHOLD = 1000000


class ListEditor:
    def __init__(self):
        self.memory = Memory()
        self.lock = threading.Lock()

    def edit_list(self, editor_name):
        with self.lock:
            if editor_name == "hammer":
                self.memory.access(3)
                self.memory.access(5)
            elif editor_name == "display":
                print("Access Count: " + str(self.memory.get_access_count(3) + self.memory.get_access_count(5)) + " "
                      + str(self.memory.__memory__[4].did_flip))
                print("6 did flip:", self.memory.__memory__[6].did_flip)

def hammer(list_editor):  # Simulate hammering behavior
    list_editor.edit_list("hammer")
    threading.Timer(1, hammer, args=(list_editor,)).start()


def display(list_editor):
    # Implement your logic for editing the list in function 2
    list_editor.edit_list("display")
    threading.Timer(5, display, args=(list_editor,)).start()


def main():
    list_editor = ListEditor()

    # Create threads
    thread1 = threading.Thread(target=hammer, args=(list_editor,))
    thread2 = threading.Thread(target=display, args=(list_editor,))

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
