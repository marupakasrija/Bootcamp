def get_integer_input():
    while True:
        user_input = input("Enter an integer: ")
        try:
            number = int(user_input)
            return number
        except ValueError:
            print("Invalid input. Please enter a whole number.")

result = get_integer_input()
print(f"You entered: {result}")