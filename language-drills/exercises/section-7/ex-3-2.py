def process_item(item_id):
    print(f"Processing item: {item_id}")
    breakpoint()  # Execution will pause here (Python 3.7+)
    result = f"Processed {item_id}"
    print(f"Result: {result}")
    return result

if __name__ == "__main__":
    process_item(10)