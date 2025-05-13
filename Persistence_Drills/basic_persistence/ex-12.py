import pickle
import os

class Parent:
    def __init__(self, name):
        self.name = name
        self.child = None # Reference to a Child object

    def set_child(self, child):
        self.child = child
        # If the relationship is bidirectional, the child must also reference the parent
        if child and child.parent != self:
             child.set_parent(self) # Ensure the back-reference is set

    def __repr__(self):
        # Be careful with __repr__ in objects with cycles, it could lead to infinite recursion
        # if you print the child's parent directly.
        # Print the child's name instead of the child object itself to break the cycle in representation.
        child_name = self.child.name if self.child else "None"
        return f"Parent(name='{self.name}', child_name='{child_name}')"

class Child:
    def __init__(self, name):
        self.name = name
        self.parent = None # Reference to a Parent object

    def set_parent(self, parent):
        self.parent = parent
        # If the relationship is bidirectional, the parent must also reference the child
        if parent and parent.child != self:
            parent.set_child(self) # Ensure the back-reference is set

    def __repr__(self):
         # Print the parent's name instead of the parent object itself
        parent_name = self.parent.name if self.parent else "None"
        return f"Child(name='{self.name}', parent_name='{parent_name}')"

# --- Simulation ---

# Create objects with cyclic references
parent_obj = Parent("Dad")
child_obj = Child("Son")

# Establish the cyclic reference using the setter methods
parent_obj.set_child(child_obj)
# The set_child method on Parent calls set_parent on Child, creating the cycle.

print("Original Objects with Cyclic References:")
print(f"Parent: {parent_obj}")
print(f"Child: {child_obj}")
print(f"Parent's child's parent is Parent: {parent_obj.child.parent is parent_obj}")
print(f"Child's parent's child is Child: {child_obj.parent.child is child_obj}")


# Save the objects using Pickle
save_file = "cyclic_objects.pkl"
try:
    with open(save_file, 'wb') as f:
        # Pickle handles the graph of objects and their references
        pickle.dump((parent_obj, child_obj), f)
    print(f"\nCyclic objects saved to {save_file}")
except Exception as e:
    print(f"Error saving cyclic objects: {e}")


# Load the objects using Pickle
try:
    with open(save_file, 'rb') as f:
        loaded_parent, loaded_child = pickle.load(f)

    print("\nLoaded Objects with Cyclic References:")
    print(f"Loaded Parent: {loaded_parent}")
    print(f"Loaded Child: {loaded_child}")

    # Verify the cyclic references are restored correctly
    print(f"Loaded Parent's child is loaded Child: {loaded_parent.child is loaded_child}")
    print(f"Loaded Child's parent is loaded Parent: {loaded_child.parent is loaded_parent}")
    print(f"Loaded Parent's child's parent is Loaded Parent: {loaded_parent.child.parent is loaded_parent}")
    print(f"Loaded Child's parent's child is Loaded Child: {loaded_child.parent.child is loaded_child}")


except FileNotFoundError:
    print(f"Error: Save file {save_file} not found.")
except Exception as e:
    print(f"Error loading cyclic objects: {e}")

# Clean up the save file (optional)
# if os.path.exists(save_file):
#     os.remove(save_file)
#     print(f"\nRemoved {save_file}")