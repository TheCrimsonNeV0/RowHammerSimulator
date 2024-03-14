import threading
import time

class ListEditor:
    def __init__(self):
        self.my_list = []
        self.lock = threading.Lock()

    def edit_list(self, editor_name):
        with self.lock:
            print(f"{editor_name} is editing the list.")
            self.my_list.append(len(self.my_list) + 1)
            print(f"{editor_name} finished editing: {self.my_list}")

def your_function1(list_editor):
    # Implement your logic for editing the list in function 1
    list_editor.edit_list("Function1")
    # Schedule next run of thread1 after 1 second
    threading.Timer(5, your_function1, args=(list_editor,)).start()

def your_function2(list_editor):
    # Implement your logic for editing the list in function 2
    list_editor.edit_list("Function2")
    # Schedule next run of thread2 after 5 seconds
    threading.Timer(5, your_function2, args=(list_editor,)).start()

def main():
    list_editor = ListEditor()

    # Start thread1 immediately
    threading.Thread(target=your_function1, args=(list_editor,)).start()

    # Start thread2 immediately
    threading.Thread(target=your_function2, args=(list_editor,)).start()

    try:
        # Keep the main thread alive to allow other threads to run
        while True:
            time.sleep(1)  # Sleep indefinitely
    except KeyboardInterrupt:
        print("Stopping threads...")
        # You can add any cleanup logic here

    # Print the final list
    print("Final List:", list_editor.my_list)

if __name__ == "__main__":
    main()
