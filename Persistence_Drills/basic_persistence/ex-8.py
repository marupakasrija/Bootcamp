import json

class User:
    def __init__(self, user_id, username, email, password_hash, session_token):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash # Sensitive
        self.session_token = session_token # Sensitive (might expire but shouldn't be logged/shared widely)

    def to_public_json(self):
        # Create a dictionary containing only non-sensitive attributes
        public_data = {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email
            # password_hash and session_token are excluded
        }
        return json.dumps(public_data, indent=4)

    def to_full_dict(self):
         # Method to get all attributes as a dictionary (useful for internal logging or specific tasks)
         return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "session_token": self.session_token
         }

    # You could also use Pickle, but remember Pickle can serialize *everything*,
    # so you need to be careful with who can deserialize it.
    # For Pickle, you might customize __getstate__ if you need to exclude attributes,
    # but the primary way is controlling what attributes exist on the object you pickle.

# Create a User object
user_instance = User(
    user_id=123,
    username="alice_wonder",
    email="alice@example.com",
    password_hash="hashed_password_123",
    session_token="abcdef123456"
)

# Get the public JSON representation
public_json = user_instance.to_public_json()
print("User object serialized to public JSON (sensitive data skipped):")
print(public_json)

# If you were to serialize the full object (e.g., for internal backup or transfer)
# full_data = user_instance.to_full_dict()
# full_json = json.dumps(full_data, indent=4)
# print("\nUser object serialized to full JSON (includes sensitive data):")
# print(full_json)