def info(name, age=0):
    print(f"Name: {name}, Age: {age}")

info(name="Bob", age=30)   # Output: Name: Bob, Age: 30
info(age=25, name="Charlie") # Output: Name: Charlie, Age: 25
info("David")              # Output: Name: David, Age: 0 (using default age)