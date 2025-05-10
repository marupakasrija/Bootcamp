# watcher.py
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .processor import process_file, update_stats # Import processing logic

class FileCreatedHandler(FileSystemEventHandler):
    """
    Custom event handler to process new files.
    """
    def __init__(self, unprocessed_dir, processed_dir, error_dir):
        self.unprocessed_dir = unprocessed_dir
        self.processed_dir = processed_dir
        self.error_dir = error_dir

    def on_created(self, event):
        if not event.is_directory:
            filepath = event.src_path
            print(f"Watcher detected new file: {filepath}")
            # Add a small delay to ensure the file is fully written
            time.sleep(0.5)
            success = process_file(filepath, self.processed_dir, self.error_dir)
            update_stats(success)


def start_watching(watch_directory: str, processed_dir: str, error_dir: str):
    """
    Starts the watchdog observer to monitor the watch directory.
    This function is blocking and keeps the script running.
    """
    event_handler = FileCreatedHandler(watch_directory, processed_dir, error_dir)
    observer = Observer()
    observer.schedule(event_handler, watch_directory, recursive=False) # Don't watch subdirectories recursively
    observer.start()
    print(f"Watcher started monitoring {watch_directory}")

    # Keep the observer running until interrupted
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("Watcher stopped.")