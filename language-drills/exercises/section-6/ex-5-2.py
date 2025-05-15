MAX_RETRIES = 3
DEFAULT_TIMEOUT_SECONDS = 10
API_ENDPOINT = "https://api.example.com/data"

def fetch_data(url, retries=MAX_RETRIES, timeout=DEFAULT_TIMEOUT_SECONDS):
    """Fetches data from the given URL with a specified number of retries and timeout."""
    for attempt in range(retries):
        print(f"Attempting to fetch data from {url}, attempt {attempt + 1}")
        # Simulate network request
        if attempt == 0:
            print("Success!")
            return {"data": "success"}
        print("Failed, retrying...")
    print("Max retries reached, failed to fetch data.")
    return None

if __name__ == "__main__":
    data = fetch_data(API_ENDPOINT)
    print(f"Fetched data: {data}")

# Original code with magic values:
# def fetch_data(url, retries=3, timeout=10):
#     for i in range(retries):
#         print(f"Attempting to fetch data from {url}, attempt {i + 1}")
#         # ...