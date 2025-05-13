import pickle

# Assuming the person_data.pkl file was created in the previous step

file_path = "person_data.pkl"

# Deserialize the object from the file
try:
    with open(file_path, 'rb') as f:
        loaded_person = pickle.load(f)

    print(f"Person object deserialized from {file_path}")
    print(loaded_person) # This will use the __str__ method
    print(f"Loaded name: {loaded_person.name}")
    print(f"Loaded education: {loaded_person.educational_institutions}")
    print(f"Loaded colleagues: {loaded_person.colleagues}")

except FileNotFoundError:
    print(f"Error: The file {file_path} was not found. Run the serialization step first.")
except Exception as e:
    print(f"An error occurred during deserialization: {e}")