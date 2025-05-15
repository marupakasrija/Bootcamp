# 08_skip_attr.py
import json
import pickle # Demonstrating pickle's __getstate__ as well

class User:
    def __init__(self, username, email, password_hash, api_key=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash # Sensitive
        self.api_key = api_key         # Sensitive
        self._internal_state = "don't show this" # Another attribute to potentially skip

    def __repr__(self):
        # Be careful not to expose sensitive data in __repr__ either
        return f"User(username='{self.username}', email='{self.email}', ...)"

    # --- For JSON/YAML (custom dictionary conversion) ---
    def to_public_dict(self):
        """
        Converts the User object to a dictionary, excluding sensitive data,
        suitable for public exposure or non-sensitive storage.
        """
        return {
            "username": self.username,
            "email": self.email
            # password_hash, api_key, _internal_state are skipped
        }

    def to_full_dict(self):
        """
        Converts the User object to a dictionary including all data,
        suitable for internal/secure storage or operations.
        """
        return {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "api_key": self.api_key,
            "_internal_state": self._internal_state
        }

    def to_public_json(self):
        """Returns the JSON string representation excluding sensitive data."""
        return json.dumps(self.to_public_dict(), indent=4)

    def to_full_json(self):
         """Returns the JSON string representation including all data."""
         return json.dumps(self.to_full_dict(), indent=4)

    # --- For Pickle (using __getstate__) ---
    def __getstate__(self):
        """
        Method called by pickle to get the state of the object to be pickled.
        We return a dictionary excluding sensitive data.
        """
        state = self.__dict__.copy() # Start with a copy of the instance's dictionary
        # Remove sensitive attributes
        state.pop('password_hash', None) # Use pop with None default to avoid error if attr is missing
        state.pop('api_key', None)
        state.pop('_internal_state', None)
        return state

    # __setstate__ is implicitly handled by pickle when __getstate__ is defined,
    # unless you need custom logic during loading.


# Create a User instance
user1 = User(
    username="secureuser",
    email="user@example.com",
    password_hash="hashed_password_123",
    api_key="sk_12345abcde"
)

print("--- JSON Serialization ---")
# Serialize excluding sensitive data using JSON
public_user_json = user1.to_public_json()
print("User object serialized (public data only JSON):")
print(public_user_json)

print("\nUser object serialized (full data JSON):")
full_user_json = user1.to_full_json()
print(full_user_json)


print("\n--- Pickle Serialization ---")
# Serialize using pickle, which will use __getstate__
pickle_file_skipped = "user_skipped_data.pkl"
try:
    with open(pickle_file_skipped, 'wb') as f:
        pickle.dump(user1, f) # pickle uses __getstate__ automatically
    print(f"Successfully serialized User object to {pickle_file_skipped} using Pickle (sensitive data skipped via __getstate__).")
except Exception as e:
    print(f"Error during pickle serialization: {e}")

# Deserialize using pickle
try:
    with open(pickle_file_skipped, 'rb') as f:
        loaded_user_pickle = pickle.load(f)

    print(f"\nSuccessfully deserialized User object from {pickle_file_skipped} using Pickle.")
    print(f"Username: {loaded_user_pickle.username}")
    print(f"Email: {loaded_user_pickle.email}")
    # These attributes were skipped during pickling, so they won't exist in the loaded object
    print(f"Password Hash: {getattr(loaded_user_pickle, 'password_hash', 'Attribute Skipped/Not Present')}")
    print(f"API Key: {getattr(loaded_user_pickle, 'api_key', 'Attribute Skipped/Not Present')}")
    print(f"Internal State: {getattr(loaded_user_pickle, '_internal_state', 'Attribute Skipped/Not Present')}")

except FileNotFoundError:
    print(f"Error: Pickle file not found at {pickle_file_skipped}.")
except Exception as e:
    print(f"Error during pickle deserialization: {e}")