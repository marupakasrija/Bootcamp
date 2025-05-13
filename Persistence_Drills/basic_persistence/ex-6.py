import yaml

class Car:
    def __init__(self, make, model, year, features):
        self.make = make
        self.model = model
        self.year = year
        self.features = features

    def __repr__(self):
        return f"Car(make='{self.make}', model='{self.model}', year={self.year}, features={self.features})"

# Example YAML string (could be read from a file)
car_yaml_string = """
make: Honda
model: Civic
year: 2022
features:
  color: red
  sunroof: false
  engine: 1.5L Turbo
"""

# Deserialize the YAML string back into a Python object
# PyYAML's load can often infer the structure and create appropriate Python types (dict, list, str, int, bool, None)
# However, it won't automatically instantiate the Car class unless you configure a custom tagger.
# For simple data, it will likely return a dictionary. We then manually create the Car object.

data = yaml.safe_load(car_yaml_string)

# Create a Car object from the loaded data (which is a dictionary)
loaded_car = Car(
    make=data.get("make"),
    model=data.get("model"),
    year=data.get("year"),
    features=data.get("features", {})
)

print("Car object deserialized from YAML string:")
print(loaded_car)
print(f"Loaded make: {loaded_car.make}")
print(f"Loaded features: {loaded_car.features}")

# Example of reading from a file (assuming car_data.yaml exists)
# try:
#     file_path = "car_data.yaml"
#     with open(file_path, 'r') as f:
#         file_yaml_string = f.read()
#     file_data = yaml.safe_load(file_yaml_string)
#     loaded_car_from_file = Car(
#         make=file_data.get("make"),
#         model=file_data.get("model"),
#         year=file_data.get("year"),
#         features=file_data.get("features", {})
#     )
#     print(f"\nCar object deserialized from file {file_path}:")
#     print(loaded_car_from_file)
# except FileNotFoundError:
#     print(f"\n{file_path} not found. Skipping file deserialization example.")