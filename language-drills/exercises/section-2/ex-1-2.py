my_dict = {"name": "Bob", "age": 25}
key_to_check = "age"
key_not_present = "city"

# LBYL
if key_to_check in my_dict:
    age = my_dict[key_to_check]
    print(f"Age (LBYL): {age}")
else:
    print(f"Key '{key_to_check}' not found.")

if key_not_present in my_dict:
    city = my_dict[key_not_present]
    print(f"City (LBYL): {city}")
else:
    print(f"Key '{key_not_present}' not found.")

# EAFP (for comparison)
try:
    age_eafp = my_dict["age"]
    print(f"Age (EAFP): {age_eafp}")
except KeyError:
    print(f"Key '{key_to_check}' not found (EAFP).")

try:
    city_eafp = my_dict["city"]
    print(f"City (EAFP): {city_eafp}")
except KeyError:
    print(f"Key '{key_not_present}' not found (EAFP).")