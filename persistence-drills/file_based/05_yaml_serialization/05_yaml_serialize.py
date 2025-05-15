# 05_yaml_serialize.py
import yaml

# Requires PyYAML: pip install PyYAML

class Car:
    def __init__(self, make, model, year, color=None, features=None):
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.features = features if features is not None else []

    def to_dict(self):
         """Converts the Car object to a dictionary suitable for YAML serialization."""
         return {
             "make": self.make,
             "model": self.model,
             "year": self.year,
             "color": self.color,
             "features": self.features
         }

# Create a Car instance
car1 = Car(
    make="Tesla",
    model="Model 3",
    year=2023,
    color="Red",
    features=["Autopilot", "Panoramic Roof", "Heated Seats"]
)

# Define the filename
yaml_file = "car_data.yaml"

# Serialize the object to a YAML string
# Use to_dict() as yaml.dump works well with dictionaries/lists
car_yaml_string = yaml.dump(car1.to_dict(), indent=2, default_flow_style=False)

print("Car object serialized to YAML string:")
print(car_yaml_string)

# Serialize the object directly to a file
try:
    # Use 'w' mode for writing in text mode
    with open(yaml_file, 'w') as f:
        yaml.dump(car1.to_dict(), f, indent=2, default_flow_style=False)
    print(f"\nSuccessfully serialized Car object to {yaml_file}")
except Exception as e:
    print(f"Error during YAML serialization: {e}")