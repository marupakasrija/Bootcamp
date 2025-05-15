class GreeterCallable:
    def __init__(self, greeting="Hello"):
        self.greeting = greeting

    def __call__(self, name):
        return f"{self.greeting}, {name}!"

greet_callable = GreeterCallable("Greetings")
print(greet_callable("Alice"))