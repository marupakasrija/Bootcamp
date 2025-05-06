import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def greet(name):
    logger.info(f"Greeting user: {name}")
    # Previously: print(f"Hello, {name}!")

def farewell(name):
    logger.info(f"Saying goodbye to: {name}")
    # Previously: print(f"Goodbye, {name}.")

if __name__ == "__main__":
    greet("Charlie")
    farewell("David")