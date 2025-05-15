import os
import time
import threading

filename = "temp_file.txt"

def try_open():
    if os.path.exists(filename):
        print(f"Thread {threading.current_thread().name}: File exists, attempting to open...")
        try:
            with open(filename, 'w') as f:
                f.write("Data")
            print(f"Thread {threading.current_thread().name}: File opened and written to.")
        except Exception as e:
            print(f"Thread {threading.current_thread().name}: Error opening file: {e}")
    else:
        print(f"Thread {threading.current_thread().name}: File does not exist.")

def delete_file():
    time.sleep(0.1)  # Give the other thread a chance to check
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Thread {threading.current_thread().name}: File deleted.")

# Create the file initially
with open(filename, 'w') as f:
    pass

thread1 = threading.Thread(target=try_open, name="Thread-1")
thread2 = threading.Thread(target=delete_file, name="Thread-2")

thread1.start()
thread2.start()

thread1.join()
thread2.join()