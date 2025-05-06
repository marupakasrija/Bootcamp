import time

def process_large_data():
    start_time = time.time()
    result = sum(range(1000000))
    end_time = time.time()
    duration = end_time - start_time
    print(f"Processing took {duration:.4f} seconds.")
    return result

if __name__ == "__main__":
    process_large_data()