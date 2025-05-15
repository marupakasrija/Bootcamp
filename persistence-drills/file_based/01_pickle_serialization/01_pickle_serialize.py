# 01_pickle_serialize.py
import pickle
import os

class Person:
    def __init__(self, name, institutions, colleagues=None):
        self.name = name
        self.institutions = institutions if institutions is not None else []
        self.colleagues = colleagues if colleagues is not None else []

    def __str__(self):
        return f"Person(name='{self.name}', institutions={self.institutions}, colleagues={self.colleagues})"

    def __repr__(self):
        return str(self) # Added repr for clarity

# Create a Person instance
person1 = Person(
    name="Alice",
    institutions=["University of Python", "Code Academy"],
    colleagues=["Bob", "Charlie"]
)

# Define the filename
pickle_file = "person_data.pkl"

# Serialize the object
try:
    # Use 'wb' mode for writing in binary mode
    with open(pickle_file, 'wb') as f:
        pickle.dump(person1, f)
    print(f"Successfully serialized Person object to {pickle_file}")
except Exception as e:
    print(f"Error during pickle serialization: {e}")