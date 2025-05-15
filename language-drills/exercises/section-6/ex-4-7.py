import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def some_function():
    logger.info("This log message comes from some_function in the current module.")

if __name__ == "__main__":
    logger.info("This log message is from the main execution block.")
    some_function()

# Explanation: Using __name__ as the logger name is a convention that helps in understanding
# where the log messages originate from in a larger application with multiple modules.
# When you run this script, the logger name will be '__main__'. If this code was imported
# into another module, the logger name would be the name of this file (e.g., 'ex_6_4_7').