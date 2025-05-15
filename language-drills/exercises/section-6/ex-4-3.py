import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class User:
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name

    def process(self):
        logger.info(f"Processing user: {self.id} - {self.name}")
        # ... processing logic ...
        logger.debug(f"User {self.name}'s processing completed.")

if __name__ == "__main__":
    user = User(101, "Alice")
    user.process()