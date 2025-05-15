import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def recursive_function(n, level=0):
    logger.debug(f"Call to recursive_function with n={n}, level={level}")
    if n <= 0:
        raise ValueError("n must be positive")
    if n == 1:
        return 1
    else:
        return n + recursive_function(n - 1, level + 1)

if __name__ == "__main__":
    try:
        result = recursive_function(5)
        print(f"Result: {result}")
        recursive_function(-1)
    except ValueError as e:
        logger.error(f"Caught an expected error: {e}")
        raise  # Re-raise the error after logging