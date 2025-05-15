# 02_pickle_deserialize.py
import pickle
import os

# The class definition must be available for pickle to deserialize
class Person:
    def __init__(self, name, institutions, colleagues=None):
        self.name = name
        self.institutions = institutions if institutions is not None else []
        self.colleagues = colleagues if colleagues is not None else []

    def __str__(self):
        return f"Person(name='{self.name}', institutions={self.institutions}, colleagues={self.colleagues})"

    def __repr__(self):
        return str(self)

# Define the filename used for serialization
pickle_file = "person_data.pkl"

# Deserialize the object
try:
    # Use 'rb' mode for reading in binary mode
    with open(pickle_file, 'rb') as f:
        loaded_person = pickle.load(f)

    print(f"Successfully deserialized Person object from {pickle_file}")
    print("Deserialized object details:")
    print(loaded_person)
    print(f"Type of loaded object: {type(loaded_person)}")
    print(f"Name: {loaded_person.name}")
    print(f"Institutions: {loaded_person.institutions}")
    print(f"Colleagues: {loaded_person.colleagues}")

except FileNotFoundError:
    print(f"Error: Serialization file not found at {pickle_file}. Please run 01_pickle_serialize.py first.")
except Exception as e:
    print(f"Error during pickle deserialization: {e}")