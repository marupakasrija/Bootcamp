import json
import os

# --- Version 1 of the class ---
class OldProduct:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def to_json(self):
        return json.dumps({"name": self.name, "price": self.price})

    def __str__(self):
        return f"OldProduct(Name: {self.name}, Price: {self.price})"

# Create and save data using Version 1
old_product = OldProduct("Laptop", 1200.00)
old_data_file = "product_v1.json"
with open(old_data_file, 'w') as f:
    f.write(old_product.to_json())
print(f"Saved old product data (v1) to {old_data_file}")

# --- Simulate a version change in the class ---
# Now, let's imagine we update the class to include a description and a version number.

class NewProduct:
    def __init__(self, name, price, description="", version=2):
        self.name = name
        self.price = price
        self.description = description
        self.version = version # Add a version attribute

    def to_json(self):
        return json.dumps({
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "version": self.version
        })

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        # Check the version of the data being loaded
        version = data.get("version", 1) # Default to version 1 if not present

        if version == 1:
            # Handle data from the old version
            print("Loading old version (v1) data...")
            return cls(
                name=data.get("name"),
                price=data.get("price"),
                # New attributes need default values or be inferred
                description="No description provided (from v1 data)"
                # The 'version' attribute will be set to the default (2) by __init__
            )
        elif version == 2:
            # Handle data from the current version
            print("Loading current version (v2) data...")
            return cls(
                name=data.get("name"),
                price=data.get("price"),
                description=data.get("description", "")
            )
        else:
            raise ValueError(f"Unknown data version: {version}")

    def __str__(self):
        return (f"NewProduct(Name: {self.name}, Price: {self.price}, "
                f"Description: '{self.description}', Version: {self.version})")

# --- Attempt to load the old data using the new class ---

try:
    with open(old_data_file, 'r') as f:
        old_json_string = f.read()

    loaded_product = NewProduct.from_json(old_json_string)
    print("\nLoaded product using the new class:")
    print(loaded_product)

except FileNotFoundError:
    print(f"Error: Old data file {old_data_file} not found.")
except ValueError as e:
    print(f"Error loading data: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Clean up the old data file (optional)
# if os.path.exists(old_data_file):
#     os.remove(old_data_file)
#     print(f"\nRemoved {old_data_file}")