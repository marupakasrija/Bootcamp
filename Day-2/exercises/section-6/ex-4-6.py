import logging

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

def application_flow():
    logger.debug("Application started")
    logger.info("Performing initial setup")
    logger.warning("Low disk space detected")
    logger.error("Failed to connect to external service")
    logger.debug("Application finished")

if __name__ == "__main__":
    application_flow()
    print("Check the 'app.log' file for output.")