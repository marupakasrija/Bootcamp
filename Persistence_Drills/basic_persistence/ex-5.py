import yaml

class Car:
    def __init__(self, make, model, year, features):
        self.make = make
        self.model = model
        self.year = year
        self.features = features # Dictionary of features

    # PyYAML can often serialize instances of simple classes directly
    # if they just contain basic data types. No explicit method needed here
    # unless you need custom logic.

    def __repr__(self):
        return f"Car(make='{self.make}', model='{self.model}', year={self.year}, features={self.features})"

# Create a Car object
car_instance = Car(
    make="Toyota",
    model="Camry",
    year=2020,
    features={"color": "blue", "sunroof": True, "engine": "2.5L"}
)

# Serialize the object to a YAML string
# Using default_flow_style=False for block style (more human-readable)
car_yaml_string = yaml.dump(car_instance, default_flow_style=False)

print("Car object serialized to YAML string:")
print(car_yaml_string)

# You can also dump directly to a file
# file_path = "car_data.yaml"
# with open(file_path, 'w') as f:
#     yaml.dump(car_instance, f, default_flow_style=False)
# print(f"Car data saved to {file_path}")