# 06_yaml_deserialize.py
import yaml

# Requires PyYAML: pip install PyYAML

# The class definition must be available
class Car:
    def __init__(self, make, model, year, color=None, features=None):
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.features = features if features is not None else []

    def to_dict(self):
         return {
             "make": self.make,
             "model": self.model,
             "year": self.year,
             "color": self.color,
             "features": self.features
         }

    @classmethod
    def from_dict(cls, data):
        """Creates a Car instance from a dictionary."""
        if isinstance(data, dict) and 'make' in data and 'model' in data and 'year' in data:
             return cls(
                 make=data['make'],
                 model=data['model'],
                 year=data['year'],
                 color=data.get('color'),
                 features=data.get('features', [])
             )
        else:
            raise ValueError("Invalid data structure for Car deserialization.")

    @classmethod
    def from_yaml(cls, yaml_string):
        """Creates a Car instance from a YAML string."""
        try:
            data = yaml.safe_load(yaml_string) # Use safe_load for security
            return cls.from_dict(data)
        except yaml.YAMLError as e:
            print(f"Error decoding YAML string: {e}")
            return None
        except ValueError as e:
            print(f"Error creating Car object from YAML: {e}")
            return None
        except Exception as e:
             print(f"An unexpected error occurred during deserialization: {e}")
             return None


# Load YAML string from car_data.yaml created by 05
yaml_file = "car_data.yaml"
car_yaml_string = None
try:
    with open(yaml_file, 'r') as f:
        car_yaml_string = f.read()
    print(f"Read YAML string from {yaml_file}")
except FileNotFoundError:
    print(f"Error: YAML file not found at {yaml_file}. Please run 05_yaml_serialize.py first.")
except Exception as e:
    print(f"Error reading YAML file: {e}")

# Deserialize the YAML string back into a Car object
loaded_car = None
if car_yaml_string:
    loaded_car = Car.from_yaml(car_yaml_string)

if loaded_car:
    print("\nSuccessfully deserialized YAML string into a Car object:")
    print(f"Make: {loaded_car.make}")
    print(f"Model: {loaded_car.model}")
    print(f"Year: {loaded_car.year}")
    print(f"Color: {loaded_car.color}")
    print(f"Features: {loaded_car.features}")
    print(f"Type of loaded object: {type(loaded_car)}")
else:
    print("\nFailed to deserialize YAML string.")