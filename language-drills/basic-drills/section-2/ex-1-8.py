def process_string(data):
    if isinstance(data, str):
        print(f"Length of the string: {len(data)}")
        print(f"Uppercase version: {data.upper()}")
    else:
        print("Error: Input must be a string.")

process_string("hello")
process_string(123)