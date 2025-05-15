import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_data(item):
    logger.info(f"Processing item: {item}")
    return f"Processed {item}"

if __name__ == "__main__":
    result = process_data("record1")
    logger.info(f"Processing result: {result}")