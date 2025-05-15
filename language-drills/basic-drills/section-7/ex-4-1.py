import logging
import uuid

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(user_id)s - %(funcName)s - %(message)s')
logger = logging.getLogger(__name__)

class UserProcessor:
    def __init__(self, user_id):
        self.user_id = user_id

    def process_data(self, data_item):
        logger.info(f"Processing data: {data_item}", extra={'user_id': self.user_id})
        # ... process data ...
        return f"Processed {data_item} for user {self.user_id}"

def main():
    user_processor = UserProcessor(user_id=uuid.uuid4())
    result = user_processor.process_data("important_record")
    print(result)

if __name__ == "__main__":
    main()