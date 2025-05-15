# 12_cyclic_ref.py
import pickle
import os
import json # To discuss how JSON *doesn't* handle cyclic refs easily

class Parent:
    def __init__(self, name):
        self.name = name
        self.child = None # Reference to Child object

    def set_child(self, child):
        self.child = child

    def __repr__(self):
        # Avoid infinite recursion in repr by not repr-ing the child directly.
        # Instead, show a representation of the child or its identifier.
        child_info = f"Child(id={self.child.child_id})" if self.child else "None"
        return f"Parent(name='{self.name}', child={child_info})"

class Child:
    def __init__(self, child_id):
        self.child_id = child_id
        self.parent = None # Reference back to Parent object

    def set_parent(self, parent):
        self.parent = parent

    def __repr__(self):
        # Avoid infinite recursion in repr by not repr-ing the parent directly.
        parent_info = f"Parent(name='{self.parent.name}')" if self.parent else "None"
        return f"Child(id={self.child_id}, parent={parent_info})"

# Create objects with cyclic references
parent = Parent("Dad")
child = Child(1)

# Establish the cyclic reference
parent.set_child(child)
child.set_parent(parent)

print("Objects with cyclic references created:")
print(parent)
print(child)
print(f"Are parent.child and child the same object? {parent.child is child}")
print(f"Are child.parent and parent the same object? {child.parent is parent}")


print("\n--- Pickle Example (Handles Cyclic References) ---")
# Serialize using Pickle - it handles cyclic references automatically
pickle_file_cyclic = "cyclic_objects.pkl"

try:
    # When we pickle 'parent', pickle detects that 'child' is already part
    # of the object graph being serialized (because parent.child is 'child').
    # When it encounters 'child' again via 'child.parent', it recognizes it
    # and inserts a reference to the already serialized 'child' object,
    # preventing infinite recursion and correctly restoring the link.
    with open(pickle_file_cyclic, 'wb') as f:
        pickle.dump(parent, f) # Pickling one object is enough to save the connected graph
    print(f"Successfully serialized cyclic objects to {pickle_file_cyclic} using Pickle.")
except Exception as e:
    print(f"Error during pickle serialization: {e}")

# Deserialize using Pickle
try:
    with open(pickle_file_cyclic, 'rb') as f:
        loaded_parent = pickle.load(f)

    print(f"\nSuccessfully deserialized cyclic objects from {pickle_file_cyclic} using Pickle.")
    print("Checking loaded objects and their references:")
    print(loaded_parent)
    loaded_child = loaded_parent.child
    print(loaded_child)

    # Verify the cyclic reference is restored correctly
    print(f"Are loaded_parent.child and loaded_child the same object? {loaded_parent.child is loaded_child}")
    print(f"Are loaded_child.parent and loaded_parent the same object? {loaded_child.parent is loaded_parent}")

except FileNotFoundError:
     print(f"Error: Pickle file not found at {pickle_file_cyclic}. Please run the pickle serialization step.")
except Exception as e:
     print(f"Error during pickle deserialization: {e}")


print("\n--- JSON Example (Does NOT Handle Cyclic References Natively) ---")

# How you might try to serialize to JSON (will cause error)
class ParentJson:
    def __init__(self, name):
        self.name = name
        self.child = None # Reference to ChildJson object

    def set_child(self, child):
        self.child = child

    def to_dict(self):
        # This will cause recursion if child.parent tries to call to_dict on self
        return {
            "name": self.name,
            "child": self.child.to_dict() if self.child else None
        }

class ChildJson:
    def __init__(self, child_id):
        self.child_id = child_id
        self.parent = None # Reference back to ParentJson object

    def set_parent(self, parent):
        self.parent = parent

    def to_dict(self):
        # This will cause recursion if parent.child tries to call to_dict on self
        return {
            "id": self.child_id,
            "parent": self.parent.to_dict() if self.parent else None # Problem here!
        }

parent_json = ParentJson("Mom")
child_json = ChildJson(2)

parent_json.set_child(child_json)
child_json.set_parent(parent_json)

try:
    print("\nAttempting to serialize objects with cyclic references using JSON.dumps...")
    # This will raise a RecursionError
    json_string_cyclic = json.dumps(parent_json.to_dict(), indent=4)
    print(json_string_cyclic) # This line won't be reached
except RecursionError:
    print("Successfully caught RecursionError! JSON.dumps cannot handle cyclic references via simple to_dict.")
except Exception as e:
    print(f"Caught unexpected error during JSON serialization attempt: {e}")

# To handle cyclic references with JSON/YAML, you'd need a more advanced approach,
# e.g., replacing object references with unique IDs and reconstructing relationships manually
# during deserialization. This often requires traversing the object graph and keeping
# track of objects already processed. This is significantly more involved than using Pickle.

# Clean up (optional)
# import os
# try:
#      os.remove(pickle_file_cyclic)
#      print(f"\nCleaned up {pickle_file_cyclic}.")
# except OSError as e:
#      print(f"Error removing file {pickle_file_cyclic}: {e}")