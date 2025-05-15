import json
import csv
import pickle
import datetime
from collections import namedtuple
from pathlib import Path
import tempfile
import shutil

# Create a temporary directory for serialization files
temp_dir_serialize = Path(tempfile.mkdtemp(prefix="serialize_"))
print(f"Created temporary directory for serialization: {temp_dir_serialize}")


# --- JSON Dump/Load ---
python_dict = {"name": "Alice", "age": 30, "city": "New York", "isStudent": False, "courses": None}
print(f"\nOriginal Python dict: {python_dict}")

json_string = json.dumps(python_dict)
print(f"JSON string (dumps): {json_string}")

deserialized_dict = json.loads(json_string)
print(f"Deserialized Python dict (loads): {deserialized_dict}")
print(f"Are original and deserialized dicts equal? {python_dict == deserialized_dict}")

# --- Pretty Print JSON ---
pretty_json_string = json.dumps(python_dict, indent=4, sort_keys=True)
print("\nPretty Printed JSON:")
print(pretty_json_string)

# --- CSV Read ---
csv_file_path_read = temp_dir_serialize / "data.csv"
# Create a dummy data.csv for reading
csv_data_to_write = [
    ["Name", "Age", "City"],
    ["Bob", "25", "London"],
    ["Charlie", "35", "Paris"]
]
with open(csv_file_path_read, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_data_to_write)

print(f"\nCSV Read (from {csv_file_path_read.name}):")
try:
    with open(csv_file_path_read, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            print(dict(row)) # Convert OrderedDict row to dict for cleaner print
except FileNotFoundError:
    print(f"Error: {csv_file_path_read} not found.")

# --- CSV Write ---
list_of_dicts_to_write = [
    {'id': 1, 'product': 'Laptop', 'price': 1200},
    {'id': 2, 'product': 'Mouse', 'price': 25},
    {'id': 3, 'product': 'Keyboard', 'price': 75}
]
csv_file_path_write = temp_dir_serialize / "output.csv"
headers = ['id', 'product', 'price']

with open(csv_file_path_write, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(list_of_dicts_to_write)
print(f"\nCSV Write: Data written to {csv_file_path_write.name}")
print(f"Content of {csv_file_path_write.name}:\n{csv_file_path_write.read_text()}")

# --- Pickle a Python Object ---
simple_object = {"a": [1, 2, 3], "b": "hello pickle", "c": (4, 5)}
pickle_file_path = temp_dir_serialize / "data.pkl"

print(f"\nPickling object: {simple_object}")
# Dump (serialize)
with open(pickle_file_path, "wb") as f: # wb for write bytes
    pickle.dump(simple_object, f)

# Load (deserialize)
with open(pickle_file_path, "rb") as f: # rb for read bytes
    loaded_object = pickle.load(f)
print(f"Unpickled object: {loaded_object}")
print(f"Are original and loaded objects equal? {simple_object == loaded_object}")


# --- Secure Unpickling ---
print("\nSecure Unpickling Discussion:")
print("DANGER: Unpickling data from untrusted sources is insecure. Pickle can execute arbitrary code.")
print("If a malicious pickle file is loaded, it can harm your system.")
print("Alternatives for data interchange with untrusted sources:")
print("1. JSON: Widely used, human-readable, limited to basic data types. Generally safe.")
print("2. XML: Another structured data format, more verbose than JSON.")
print("3. MessagePack, Protocol Buffers, Avro: Binary serialization formats, efficient and often schema-based.")
print("4. `ast.literal_eval` for simple Python literal structures if you MUST evaluate a string from an untrusted source (safer than `eval`).")
print("   However, for general data serialization, JSON is preferred over `literal_eval`.")
print("Example: Using JSON instead of pickle for data exchange.")
data_for_json = {"key": "value", "numbers": [1,2,3]}
safe_serialized = json.dumps(data_for_json)
safe_deserialized = json.loads(safe_serialized)
print(f"Safely serialized with JSON: {safe_serialized}")
print(f"Safely deserialized with JSON: {safe_deserialized}")
# Marshal: The marshal module is primarily used by Python for its .pyc files and is not intended for general-purpose serialization
# or communication with untrusted sources. It also has security implications similar to pickle, though perhaps less exploited.
# It's generally not considered a "safe alternative" for untrusted data.

# --- Custom JSON Encoder ---
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

data_with_datetime = {
    "event": "Meeting",
    "timestamp": datetime.datetime(2025, 5, 6, 10, 30, 0),
    "reminder_date": datetime.date(2025, 5, 5)
}
print("\nCustom JSON Encoder for datetime:")
json_with_custom_encoder = json.dumps(data_with_datetime, cls=DateTimeEncoder, indent=2)
print(json_with_custom_encoder)
# To decode, you'd need a custom object_hook in json.loads
def datetime_decoder(dct):
    for k, v in dct.items():
        if isinstance(v, str):
            try:
                # Attempt to parse as datetime, then date
                dt_obj = datetime.datetime.fromisoformat(v)
                dct[k] = dt_obj
            except ValueError:
                try:
                    d_obj = datetime.date.fromisoformat(v)
                    dct[k] = d_obj
                except ValueError:
                    pass # Not an isoformat date/datetime string
    return dct

decoded_with_hook = json.loads(json_with_custom_encoder, object_hook=datetime_decoder)
print("Decoded with custom hook:")
print(decoded_with_hook)
print(f"Type of 'timestamp': {type(decoded_with_hook['timestamp'])}")
print(f"Type of 'reminder_date': {type(decoded_with_hook['reminder_date'])}")


# --- Read CSV into NamedTuples ---
Product = namedtuple("Product", ["name", "category", "price"])
csv_for_namedtuple_path = temp_dir_serialize / "products.csv"
# Create dummy products.csv
with open(csv_for_namedtuple_path, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Product Name", "Category", "Price"]) # Header
    writer.writerow(["Laptop X1", "Electronics", "1200.50"])
    writer.writerow(["Coffee Beans", "Groceries", "15.75"])
    writer.writerow(["Python Book", "Books", "45.00"])

print(f"\nRead CSV into NamedTuples (from {csv_for_namedtuple_path.name}):")
products_list = []
try:
    with open(csv_for_namedtuple_path, mode='r', newline='') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader) # Skip header row
        # Dynamically create NamedTuple based on CSV header (optional, for robustness)
        # Record = namedtuple("Record", [col.replace(" ", "_").lower() for col in header])
        for row in csv_reader:
            # Assuming fixed structure for this example: name, category, price
            # Convert price to float
            try:
                product = Product(row[0], row[1], float(row[2]))
                products_list.append(product)
            except (IndexError, ValueError) as e:
                print(f"Skipping row due to error: {row} - {e}")

    for p in products_list:
        print(f"Name: {p.name}, Category: {p.category}, Price: ${p.price:.2f}")
except FileNotFoundError:
    print(f"Error: {csv_for_namedtuple_path} not found.")


# --- Clean up the serialization temporary directory ---
try:
    shutil.rmtree(temp_dir_serialize)
    print(f"\nCleaned up temporary directory for serialization: {temp_dir_serialize}")
except Exception as e:
    print(f"Error cleaning up temp directory {temp_dir_serialize}: {e}")