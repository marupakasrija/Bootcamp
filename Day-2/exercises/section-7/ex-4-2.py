import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(funcName)s - %(duration)s ms - %(message)s')
logger = logging.getLogger(__name__)

def calculate_something():
    start_time = time.time()
    # Simulate some time-consuming operation
    time.sleep(0.5)
    end_time = time.time()
    duration_ms = (end_time - start_time) * 1000
    logger.info("Calculation finished", extra={'duration': f"{duration_ms:.2f}"})

if __name__ == "__main__":
    calculate_something()