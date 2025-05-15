import logging

debug = True  # Set this flag to True to enable debug logging

logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
logger = logging.getLogger(__name__)

def process_item(item_id, data):
    logger.info(f"Processing item with ID: {item_id}")
    if debug:
        logger.debug(f"Item {item_id} data: {data}")
    # ... actual processing ...
    result = f"Processed item {item_id}"
    logger.info(f"Finished processing item with ID: {item_id}")
    return result

if __name__ == "__main__":
    item = {"name": "example", "value": 10}
    process_item(1, item)