import subprocess
import threading
import multiprocessing
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os
import sys

# --- Run a Command ---
# Unix-like: ls -l. Windows: dir
command = ["ls", "-l"] if sys.platform != "win32" else ["dir"]
print(f"\nRunning command: {' '.join(command)}")
try:
    # For just running and seeing output on console, no capture:
    # subprocess.run(command, check=True) # check=True will raise CalledProcessError on non-zero exit
    # For capturing output, see next section.
    # This simplified run will just execute, output goes to stdout/stderr of this script.
    result_run = subprocess.run(command, text=True) # text=True decodes stdout/stderr
    print(f"Command executed. Return code: {result_run.returncode}")
except FileNotFoundError:
    print(f"Error: Command '{command[0]}' not found. Ensure it's in your PATH.")
except subprocess.CalledProcessError as e:
    print(f"Command failed with error: {e}")


# --- Capture Output ---
command_capture = ["echo", "Hello from subprocess"] if sys.platform != "win32" else ["cmd", "/c", "echo Hello from subprocess"]
print(f"\nRunning command and capturing output: {' '.join(command_capture)}")
try:
    result_capture = subprocess.run(command_capture, capture_output=True, text=True, check=True)
    print(f"Captured STDOUT:\n{result_capture.stdout.strip()}")
    if result_capture.stderr:
        print(f"Captured STDERR:\n{result_capture.stderr.strip()}")
except FileNotFoundError:
    print(f"Error: Command '{command_capture[0]}' not found.")
except subprocess.CalledProcessError as e:
    print(f"Command failed with error: {e}")
    print(f"STDOUT: {e.stdout}")
    print(f"STDERR: {e.stderr}")


# --- Check Exit Code ---
command_fail = ["ls", "/nonexistentfolder"] if sys.platform != "win32" else ["cmd", "/c", "dir", "Z:\\nonexistentfolder"] # This will likely fail
print(f"\nRunning a command expected to fail: {' '.join(command_fail)}")
try:
    # We don't use check=True here because we want to inspect the return code manually
    result_fail = subprocess.run(command_fail, capture_output=True, text=True)
    print(f"Command finished. Return code: {result_fail.returncode}")
    if result_fail.returncode != 0:
        print("Subprocess failed!")
        print(f"Error output (stderr):\n{result_fail.stderr.strip()}")
    else:
        print("Subprocess succeeded (unexpectedly for this example).")
except FileNotFoundError:
    print(f"Error: Command '{command_fail[0]}' not found.")


# --- Start a Thread ---
print("\nStarting a Thread:")
def print_numbers_threaded():
    print("Thread: Starting to print numbers.")
    for i in range(1, 4):
        print(f"Thread: {i}")
        time.sleep(0.3)
    print("Thread: Finished printing numbers.")

thread = threading.Thread(target=print_numbers_threaded)
thread.start()
print("Main: Thread started. Waiting for it to complete...")
thread.join() # Wait for the thread to finish
print("Main: Thread has completed.")

# --- Start a Process ---
print("\nStarting a Process:")
def cpu_bound_task(n):
    print(f"Process {os.getpid()}: Starting CPU bound task for {n}.")
    sum_val = sum(i*i for i in range(n))
    print(f"Process {os.getpid()}: Finished. Sum of squares up to {n-1} is {sum_val}.")
    return sum_val

if __name__ == "__main__": # Guard for multiprocessing on Windows/some setups
    process = multiprocessing.Process(target=cpu_bound_task, args=(100000,)) # Relatively small for quick demo
    process.start()
    print("Main: Process started. Waiting for it to complete...")
    process.join()
    print("Main: Process has completed.")

# --- Thread Locking ---
print("\nThread Locking:")
shared_variable = 0
lock = threading.Lock()
num_increments = 100000

def increment_shared_var():
    global shared_variable
    for _ in range(num_increments):
        with lock: # Acquire and release lock automatically
            shared_variable += 1

def increment_shared_var_no_lock(): # For comparison of race condition
    global shared_variable_no_lock
    for _ in range(num_increments):
        shared_variable_no_lock +=1


thread1 = threading.Thread(target=increment_shared_var)
thread2 = threading.Thread(target=increment_shared_var)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
print(f"Main: Shared variable with lock: {shared_variable} (Expected: {2 * num_increments})")

# Demonstrate without lock (will likely be incorrect)
if __name__ == "__main__": # Guard for potential re-runs or imports
    shared_variable_no_lock = 0
    thread3 = threading.Thread(target=increment_shared_var_no_lock)
    thread4 = threading.Thread(target=increment_shared_var_no_lock)
    thread3.start()
    thread4.start()
    thread3.join()
    thread4.join()
    print(f"Main: Shared variable WITHOUT lock: {shared_variable_no_lock} (Expected: {2 * num_increments}, but likely less)")


# --- Use concurrent.futures ---
print("\nUsing concurrent.futures (ThreadPoolExecutor):")
def task_for_executor(item):
    # print(f"Thread {threading.get_ident()}: Processing item {item}")
    time.sleep(0.1)
    return item * item

items_to_process = [1, 2, 3, 4, 5, 6, 7, 8]
results_threadpool = []
with ThreadPoolExecutor(max_workers=3) as executor:
    # Submit tasks
    future_to_item = {executor.submit(task_for_executor, item): item for item in items_to_process}
    for future in future_to_item: # Iterate over futures as they complete (or in submission order)
        item = future_to_item[future]
        try:
            result = future.result() # Blocks until this future is done
            results_threadpool.append(result)
            # print(f"Item {item} processed, result: {result}")
        except Exception as exc:
            print(f"Item {item} generated an exception: {exc}")

    # Alternative: using map (simpler if order of results matters and corresponds to input order)
    # results_map = list(executor.map(task_for_executor, items_to_process))

print(f"Results from ThreadPoolExecutor: {sorted(results_threadpool)}") # Sorted because order of completion can vary

# ProcessPoolExecutor example (if the task is CPU-bound and benefits from true parallelism)
if __name__ == "__main__": # Guard for multiprocessing
    print("\nUsing concurrent.futures (ProcessPoolExecutor):")
    results_processpool = []
    try:
        with ProcessPoolExecutor(max_workers=2) as executor: # max_workers can be os.cpu_count()
            future_to_item_p = {executor.submit(cpu_bound_task, item * 10000): item for item in [1, 2, 3, 4]}
            for future in future_to_item_p:
                item_orig = future_to_item_p[future]
                try:
                    result = future.result() # Will be the sum from cpu_bound_task
                    results_processpool.append(f"Input {item_orig} -> Processed (sum: {result})")
                except Exception as exc:
                    print(f"CPU Task for input {item_orig} generated an exception: {exc}")
        print(f"Results from ProcessPoolExecutor (details printed by tasks):\n{results_processpool}")
    except RuntimeError as e:
        # This can happen if ProcessPoolExecutor is not properly guarded by if __name__ == "__main__":
        # or in some interactive environments.
        print(f"Could not run ProcessPoolExecutor example: {e}")


# --- Kill a Subprocess ---
print("\nKill a Subprocess:")
# Command that runs for a while (e.g., ping or a sleep script)
# On Windows, 'ping -n 10 localhost' pings 10 times. 'timeout 10' also works.
# On Unix, 'sleep 10'
sleep_command = ["sleep", "10"] if sys.platform != "win32" else ["timeout", "/t", "10", "/nobreak"]

print(f"Starting long-running subprocess: {' '.join(sleep_command)}")
try:
    process_to_kill = subprocess.Popen(sleep_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Subprocess started with PID: {process_to_kill.pid if process_to_kill.pid else 'N/A'}")

    kill_delay = 2 # seconds
    print(f"Waiting for {kill_delay} seconds before attempting to terminate...")
    time.sleep(kill_delay)

    # Check if process is still running
    if process_to_kill.poll() is None: # poll() returns None if process is still running
        print("Subprocess is still running. Terminating it...")
        process_to_kill.terminate() # Sends SIGTERM on Unix, TerminateProcess on Windows
        # For a more forceful kill, use process_to_kill.kill() (SIGKILL on Unix)
        process_to_kill.wait(timeout=2) # Wait for termination to complete
        print("Subprocess terminated.")
    else:
        print("Subprocess finished before termination was attempted.")

    stdout, stderr = process_to_kill.communicate() # Get any remaining output
    print(f"Subprocess return code after termination/completion: {process_to_kill.returncode}")
    # if stdout: print(f"STDOUT from killed process: {stdout.decode(errors='ignore')}")
    # if stderr: print(f"STDERR from killed process: {stderr.decode(errors='ignore')}")

except FileNotFoundError:
    print(f"Error: Command for subprocess to kill ('{sleep_command[0]}') not found.")
except subprocess.TimeoutExpired:
    print("Timeout expired while waiting for process to terminate. It might still be running or be a zombie.")
    process_to_kill.kill() # Force kill
    process_to_kill.wait()
except Exception as e:
    print(f"An error occurred during subprocess kill test: {e}")

print("\n--- End of Standard Library Mastery Section ---")

# Guard for multiprocessing examples needing to be in __main__ for some platforms
if __name__ == "__main__":
    print("\nRe-running multiprocessing examples if this script is executed directly:")
    # (The Process examples above are already guarded, this is just a structural note)
    # Example: Start a Process (if not run above due to import)
    # process = multiprocessing.Process(target=cpu_bound_task, args=(50000,))
    # process.start()
    # process.join()
    # print("Re-run Process has completed.")
    pass