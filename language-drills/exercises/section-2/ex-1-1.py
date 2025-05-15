my_dict = {"name": "Alice", "age": 30}

# LBYL (Look Before You Leap)
if "city" in my_dict:
    city = my_dict["city"]
    print(f"City (LBYL): {city}")
else:
    print("City key not found (LBYL).")

# EAFP (Easier to Ask Forgiveness than Permission)
try:
    city = my_dict["city"]
    print(f"City (EAFP): {city}")
except KeyError:
    print("City key not found (EAFP).")