import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def process_data(data):
    try:
        result = 10 / len(data)
        return result
    except TypeError as e:
        logging.error(f"TypeError occurred: {e}")
        raise  # Re-raises the caught exception
    except ZeroDivisionError as e:
        logging.error(f"ZeroDivisionError occurred: {e}")
        raise

try:
    process_data([1, 2, 3])
    process_data(None)
except TypeError as e:
    print(f"Caught in main: {e}")
except ZeroDivisionError as e:
    print(f"Caught in main: {e}")