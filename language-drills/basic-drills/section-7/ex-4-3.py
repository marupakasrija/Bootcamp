import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(error_id)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_resource(resource_id):
    try:
        # Simulate fetching a resource that might fail
        if resource_id == 404:
            raise ValueError("Resource not found")
        return f"Resource {resource_id}"
    except ValueError as e:
        error_id = "RES-404"
        logger.error(f"Error fetching resource: {e}", extra={'error_id': error_id})
        return None

if __name__ == "__main__":
    resource1 = fetch_resource(123)
    print(f"Resource 1: {resource1}")
    resource2 = fetch_resource(404)
    print(f"Resource 2: {resource2}")