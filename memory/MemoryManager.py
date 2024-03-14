import threading
import time


class MemoryManager:
    def __init__(self, memory):
        self.memory = memory
        self.lock = threading.Lock()

    def hammer(self, row):
        while True:
            with self.lock:
                self.memory.access(row)
                time.sleep(1)

    def mitigate(self):
        pass