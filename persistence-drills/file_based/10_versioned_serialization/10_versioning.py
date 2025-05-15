# 10_versioning.py
import pickle
import os
import time

# --- Version 1 of the Data Class ---
# Assume this was the original class definition
class DataV1:
    def __init__(self, value1, value2):
        self.value1 = value1
        self.value2 = value2
        # _version might not have existed in the very first version,
        # but adding it in V1 is the start of the versioning strategy.
        # For truly legacy data without _version, __setstate__ in V2
        # needs to handle the missing key gracefully (e.g., default to version 1).
        self._version = 1

    def __repr__(self):
        return f"DataV1(value1={self.value1!r}, value2={self.value2!r}, _version={self._version})"

    # No __getstate__ or __setstate__ needed for the initial version,
    # as pickle's default behavior is usually sufficient.


# Create and serialize a V1 object
data_v1 = DataV1("hello", 123)
v1_file = "data_v1.pkl"

print("--- Serializing DataV1 ---")
try:
    with open(v1_file, 'wb') as f:
        pickle.dump(data_v1, f)
    print(f"Serialized DataV1 object to {v1_file}")
except Exception as e:
    print(f"Error serializing V1 data: {e}")

# --- Simulate a version change: Introduce DataV2 ---
# Assume this code runs in a later version of your application
print("\n--- Simulating application update and defining DataV2 ---")

class DataV2:
    def __init__(self, value1, value3, new_attribute="default"):
        self.value1 = value1
        # Renamed value2 to value3 in V2
        self.value3 = value3
        self.new_attribute = new_attribute # New attribute in V2
        self._version = 2 # Update the version attribute

    def __repr__(self):
         return (f"DataV2(value1={self.value1!r}, value3={self.value3!r}, "
                 f"new_attribute={self.new_attribute!r}, _version={self._version})")

    def __getstate__(self):
        """Save state for V2."""
        state = self.__dict__.copy()
        # If you had attributes to skip, you'd do it here
        return state # Include _version in the state

    def __setstate__(self, state):
        """
        Handle loading data from different versions.
        The 'state' dictionary contains the attributes from the pickled object.
        """
        # Get the version from the state, default to 1 if not present
        # This handles data pickled before the _version attribute existed.
        version = state.get('_version', 1)
        print(f"__setstate__ called for DataV2, loading version: {version}")

        if version == 1:
            print("  Loading DataV1 data and migrating to DataV2 format.")
            # Handle migration from V1 to V2 structure
            self.value1 = state.get('value1', None) # Get old value1
            # value2 from V1 becomes value3 in V2
            self.value3 = state.get('value2', None) # Get old value2
            # Set the new attribute to its default value or a specific migration value
            self.new_attribute = "migrated_from_v1"
            self._version = 2 # Set the instance's version to the current version

        elif version == 2:
            print("  Loading DataV2 data directly.")
            # Directly update the instance's dictionary with the V2 state
            # Ensure all V2 attributes are expected
            self.__dict__.update(state)
            # If any new attributes were added in a hypothetical V3, you'd handle them here
            # by providing defaults if they are missing in the V2 state.
            # e.g., self.another_v3_attr = state.get('another_v3_attr', default_value)

        else:
            # Handle future or unknown versions - might raise an error or attempt best effort
            print(f"  Warning: Unknown data version {version}. Attempting to load directly (may fail or be incomplete).")
            self.__dict__.update(state)


# Attempt to load the V1 object using the V2 class definition
print("\n--- Loading V1 data with DataV2 class ---")
try:
    with open(v1_file, 'rb') as f:
        # Pickle looks up DataV2 by name, creates an instance, then calls __setstate__
        loaded_data_v2_from_v1 = pickle.load(f)

    print(f"Successfully loaded object (originally V1) as DataV2 from {v1_file}")
    print(loaded_data_v2_from_v1)
    print(f"Type of loaded object: {type(loaded_data_v2_from_v1)}")
    # Verify migration
    print(f"  Migrated value3: {loaded_data_v2_from_v1.value3}")
    print(f"  New attribute: {loaded_data_v2_from_v1.new_attribute}")


except FileNotFoundError:
    print(f"Error: V1 file not found at {v1_file}. Please run the V1 serialization step.")
except Exception as e:
    print(f"Error during pickle deserialization with versioning: {e}")


# --- Serialize a V2 object and load it with V2 class ---
print("\n--- Serializing and Loading DataV2 ---")
data_v2_new = DataV2("goodbye", 456, new_attribute="custom value")
v2_file = "data_v2.pkl"

try:
    with open(v2_file, 'wb') as f:
        pickle.dump(data_v2_new, f)
    print(f"Serialized DataV2 object to {v2_file}")
except Exception as e:
    print(f"Error serializing V2 data: {e}")


try:
    with open(v2_file, 'rb') as f:
        loaded_data_v2_direct = pickle.load(f)

    print(f"\nSuccessfully loaded DataV2 object as DataV2 from {v2_file}")
    print(loaded_data_v2_direct)
    print(f"Type of loaded object: {type(loaded_data_v2_direct)}")

except FileNotFoundError:
     print(f"Error: V2 file not found at {v2_file}. Please run the V2 serialization step.")
except Exception as e:
    print(f"Error during pickle deserialization: {e}")

# Clean up (optional)
# import os
# try:
#     os.remove(v1_file)
#     os.remove(v2_file)
#     print("\nCleaned up data files.")
# except OSError as e:
#     print(f"Error removing files: {e}")