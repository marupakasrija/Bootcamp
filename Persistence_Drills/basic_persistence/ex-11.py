import pickle
import os

class Item:
    def __init__(self, item_id, name):
        self.item_id = item_id
        self.name = name

    def __repr__(self):
        return f"Item(id={self.item_id}, name='{self.name}')"

class MyCollection:
    def __init__(self, name):
        self.name = name
        self.items = [] # List of Item objects
        self.metadata = {} # Dictionary for additional data

    def add_item(self, item):
        if isinstance(item, Item):
            self.items.append(item)
        else:
            print("Can only add Item objects to MyCollection.")

    def add_metadata(self, key, value):
        self.metadata[key] = value

    # With Pickle, serialization and deserialization of the MyCollection
    # instance and its contained objects (Item instances) is handled automatically
    # as long as the contained objects are also pickleable.
    # No special __getstate__/__setstate__ needed here unless you want custom logic.

    def save(self, filename):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self, f)
            print(f"Collection '{self.name}' saved to {filename}")
        except Exception as e:
            print(f"Error saving collection: {e}")

    @classmethod
    def load(cls, filename):
        if not os.path.exists(filename):
            print(f"Save file {filename} not found. Cannot load collection.")
            return None

        try:
            with open(filename, 'rb') as f:
                collection = pickle.load(f)
            print(f"Collection '{collection.name}' loaded from {filename}")
            return collection
        except Exception as e:
            print(f"Error loading collection: {e}")
            return None

    def __str__(self):
        item_list = ", ".join([str(item) for item in self.items])
        return (f"--- MyCollection: {self.name} ---\n"
                f"Items: [{item_list}]\n"
                f"Metadata: {self.metadata}\n"
                f"--------------------------")

# --- Simulation ---

# Create a collection
my_collection = MyCollection("My Precious Items")

# Add items
item1 = Item(1, "Magic Wand")
item2 = Item(2, "Healing Potion")
my_collection.add_item(item1)
my_collection.add_item(item2)

# Add metadata
my_collection.add_metadata("creator", "Merlin")
my_collection.add_metadata("version", 1.0)

print("Original Collection:")
print(my_collection)

# Save the collection
save_file = "my_collection.pkl"
my_collection.save(save_file)

# Load the collection
loaded_collection = MyCollection.load(save_file)

if loaded_collection:
    print("\nLoaded Collection:")
    print(loaded_collection)
    # Verify loaded data
    print(f"Loaded collection name: {loaded_collection.name}")
    print(f"Number of loaded items: {len(loaded_collection.items)}")
    print(f"Loaded item names: {[item.name for item in loaded_collection.items]}")
    print(f"Loaded metadata: {loaded_collection.metadata}")

# Clean up the save file (optional)
# if os.path.exists(save_file):
#     os.remove(save_file)
#     print(f"\nRemoved {save_file}")