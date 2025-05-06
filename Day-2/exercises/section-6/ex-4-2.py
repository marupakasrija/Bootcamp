import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def calculate(x, y):
    logger.debug(f"Input values: x={x}, y={y}")
    result = x + y
    logger.info(f"Calculation result: {result}")
    if result > 10:
        logger.warning("Result is greater than 10")
    return result

if __name__ == "__main__":
    calculate(5, 3)
    calculate(7, 8)
    try:
        raise ValueError("Something went wrong")
    except ValueError as e:
        logger.error(f"An error occurred: {e}")