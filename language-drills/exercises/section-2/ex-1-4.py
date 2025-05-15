class Person:
    def __init__(self, name):
        self.name = name

person1 = Person("Charlie")

# EAFP using getattr with a default value
city1 = getattr(person1, "city", "Unknown City")
print(f"{person1.name}'s city: {city1}")

# LBYL (requires checking if the attribute exists)
if hasattr(person1, "age"):
    age1 = person1.age
    print(f"{person1.name}'s age (LBYL): {age1}")
else:
    print(f"{person1.name} has no age attribute (LBYL).")