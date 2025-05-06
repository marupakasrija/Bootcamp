import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def process_user(user_id, username):
    logger.debug(f"Entering process_user with user_id: {user_id}, username: {username}")
    # Simulate some processing
    logger.debug(f"Exiting process_user for user_id: {user_id}")
    return f"Processed: {username}"

if __name__ == "__main__":
    user = {"id": 1, "name": "Alice"}
    result = process_user(user["id"], user["name"])
    logger.info(f"Processing result: {result}")