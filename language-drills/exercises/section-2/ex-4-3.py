class LogContext:
    def __enter__(self):
        print("Entering the context.")
        return self  # You can return a value that will be assigned to the 'as' variable

    def __exit__(self, exc_type, exc_value, traceback):
        print("Exiting the context.")
        if exc_type:
            print(f"An exception of type {exc_type} occurred: {exc_value}")
        return False  # Returning False re-raises the exception (if any)

with LogContext() as context:
    print("Inside the context.")
    # raise ValueError("Something went wrong!") # Uncomment to test exception handling