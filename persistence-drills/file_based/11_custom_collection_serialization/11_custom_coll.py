# 11_custom_coll.py
import pickle
import json # Using JSON for custom serialization example
import os

# Assume these classes are defined elsewhere or here
class Item:
    def __init__(self, item_id, name):
        self.item_id = item_id
        self.name = name

    def __repr__(self):
        return f"Item(id={self.item_id}, name='{self.name}')"

    # Needed for custom JSON/YAML serialization
    def to_dict(self):
        return {"id": self.item_id, "name": self.name}

    @classmethod
    def from_dict(cls, data):
        if isinstance(data, dict) and 'id' in data and 'name' in data:
            return cls(item_id=data['id'], name=data['name'])
        # Handle potential errors or return None if invalid
        print(f"Warning: Could not create Item from invalid data: {data}")
        return None


class MyCollection:
    def __init__(self, name="Default Collection"):
        self.name = name
        self._items = [] # Internal list of items
        self._metadata = {"created_at": "now"} # Example metadata

    def add_item(self, item):
        if isinstance(item, Item): # Optional: Add validation
            self._items.append(item)
        else:
            print(f"Warning: Can only add Item objects, skipping {type(item)}")


    def get_items(self):
        return self._items

    def __repr__(self):
        # Limit the number of items shown in repr for brevity
        items_repr = repr(self._items[:3]) + ('...' if len(self._items) > 3 else '')
        return f"MyCollection(name='{self.name!r}', items={items_repr}, metadata={self._metadata!r})"


    # --- Pickle Serialization ---
    # Pickle often works automatically if contents are pickleable.
    # Customizing using __getstate__ and __setstate__ is for advanced control (like versioning, skipping).

    # Example using __getstate__ (optional for this simple case)
    # def __getstate__(self):
    #     """Customize state for pickling."""
    #     state = self.__dict__.copy()
    #     # Example: modify or skip certain attributes before pickling
    #     # state['_metadata'] = {"pickled_at": time.time()}
    #     # del state['_metadata'] # To skip metadata
    #     return state

    # Example using __setstate__ (optional for this simple case)
    # def __setstate__(self, state):
    #     """Customize state loading for unpickling."""
    #     # Example: handle if _metadata was skipped or changed in an older version
    #     # if '_metadata' not in state:
    #     #     state['_metadata'] = {"notes": "metadata was missing, added default during load"}
    #     self.__dict__.update(state)


    # --- Custom Serialization (e.g., to JSON) ---
    def to_dict(self):
        """Convert collection and its contents to a dictionary for JSON/YAML."""
        return {
            "name": self.name,
            # Serialize each item using its own to_dict method
            "items": [item.to_dict() for item in self._items if hasattr(item, 'to_dict')],
            "metadata": self._metadata
        }

    def to_json(self):
        """Serialize the collection to a JSON string."""
        try:
            return json.dumps(self.to_dict(), indent=4)
        except TypeError as e:
            print(f"Error serializing to JSON: {e}. Ensure all items are serializable.")
            return None


    @classmethod
    def from_dict(cls, data):
        """Create a collection from a dictionary representation."""
        if isinstance(data, dict) and 'name' in data and 'items' in data:
            collection = cls(name=data['name'])
            # Deserialize each item using its from_dict method
            for item_data in data.get('items', []):
                item = Item.from_dict(item_data)
                if item: # Only add if deserialization was successful
                    collection.add_item(item)
            collection._metadata = data.get('metadata', {}) # Load metadata, default to empty dict
            return collection
        # Handle cases where input data is invalid
        print(f"Error: Invalid data structure for MyCollection deserialization: {data}")
        return None

    @classmethod
    def from_json(cls, json_string):
        """Deserialize a JSON string into a collection."""
        try:
            data = json.loads(json_string)
            return cls.from_dict(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON string: {e}")
            return None
        except Exception as e:
            print(f"Error deserializing collection from JSON: {e}")
            return None


# --- Usage ---

print("--- Pickle Example ---")
collection_pickle = MyCollection("Pickle Collection")
collection_pickle.add_item(Item(1, "Apple"))
collection_pickle.add_item(Item(2, "Banana"))
collection_pickle.add_item(Item(3, "Cherry")) # Add more items
collection_pickle.add_item(Item(4, "Date"))

pickle_file_collection = "collection_pickle.pkl"
try:
    with open(pickle_file_collection, 'wb') as f:
        pickle.dump(collection_pickle, f)
    print(f"Serialized MyCollection object to {pickle_file_collection} using Pickle.")
except Exception as e:
    print(f"Error during pickle serialization: {e}")

try:
    with open(pickle_file_collection, 'rb') as f:
        loaded_collection_pickle = pickle.load(f)
    print(f"\nSuccessfully deserialized MyCollection object from {pickle_file_collection} using Pickle.")
    print(loaded_collection_pickle)
    print(f"Items in loaded collection: {loaded_collection_pickle.get_items()}")
except FileNotFoundError:
     print(f"Error: Pickle file not found at {pickle_file_collection}.")
except Exception as e:
     print(f"Error during pickle deserialization: {e}")

print("\n--- JSON Example ---")
collection_json = MyCollection("JSON Collection")
collection_json.add_item(Item(10, "Orange"))
collection_json.add_item(Item(20, "Grape"))
collection_json.add_item(Item(30, "Mango"))

collection_json_string = collection_json.to_json()
if collection_json_string:
    print("Serialized MyCollection object to JSON string (custom logic):")
    print(collection_json_string)

    loaded_collection_json = MyCollection.from_json(collection_json_string)
    if loaded_collection_json:
        print("\nSuccessfully deserialized JSON string into MyCollection object (custom logic):")
        print(loaded_collection_json)
        print(f"Items in loaded collection: {loaded_collection_json.get_items()}")
    else:
        print("\nFailed to deserialize JSON string into MyCollection object.")
else:
    print("\nFailed to serialize MyCollection object to JSON.")

# Clean up (optional)
# import os
# try:
#      os.remove(pickle_file_collection)
#      print(f"\nCleaned up {pickle_file_collection}.")
# except OSError as e:
#      print(f"Error removing file {pickle_file_collection}: {e}")