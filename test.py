import threading
import time

# Initialize the shared list with length 10 and all values 0
shared_list = [0] * 10

# Lock for synchronizing access to the shared list
lock = threading.Lock()

def flip_to_1():
    while True:
        time.sleep(5)
        with lock:
            shared_list[0] = 1

def flip_to_0():
    while True:
        time.sleep(3)
        with lock:
            shared_list[0] = 0

def print_list():
    while True:
        time.sleep(1)
        with lock:
            print(shared_list)

def main():
    # Create the threads
    t1 = threading.Thread(target=flip_to_1)
    t2 = threading.Thread(target=flip_to_0)
    t3 = threading.Thread(target=print_list)

    # Start the threads
    t1.start()
    t2.start()
    t3.start()

    # Join the threads (optional, in this case it keeps the main thread alive)
    t1.join()
    t2.join()
    t3.join()

if __name__ == "__main__":
    main()