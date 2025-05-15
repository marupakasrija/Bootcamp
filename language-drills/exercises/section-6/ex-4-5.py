import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def task_start(task_name):
    logger.info(f"Starting task: {task_name}")

def task_end(task_name):
    logger.info(f"Task finished: {task_name}")

if __name__ == "__main__":
    task_start("Database Backup")
    # ... perform backup ...
    task_end("Database Backup")