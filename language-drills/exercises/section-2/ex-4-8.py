class Resource:
    def __enter__(self):
        print("Resource acquired.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("Resource released.")

def use_resource():
    with Resource() as res:
        print("Using the resource.")
        raise RuntimeError("Something went wrong while using the resource.")
        print("This line will not be reached.")

try:
    use_resource()
except RuntimeError as e:
    print(f"Caught an error: {e}")