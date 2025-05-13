import pickle

class Person:
    def __init__(self, name, educational_institutions, colleagues):
        self.name = name
        self.educational_institutions = educational_institutions # List of strings
        self.colleagues = colleagues # List of strings or Person objects (let's use strings for simplicity here)

    def __str__(self):
        return f"Person(Name: {self.name}, Education: {self.educational_institutions}, Colleagues: {self.colleagues})"

# Create a Person object
person_instance = Person(
    name="Alice",
    educational_institutions=["University A", "College B"],
    colleagues=["Bob", "Charlie"]
)

# Serialize the object using pickle
file_path = "person_data.pkl"
with open(file_path, 'wb') as f:
    pickle.dump(person_instance, f)

print(f"Person object serialized and saved to {file_path}")