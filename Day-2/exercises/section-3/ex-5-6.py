class Invoker:
    @staticmethod
    def greet(name):
        return f"Hello, {name}!"

print(f"Greeting from class: {Invoker.greet('Charlie')}")
invoker_instance = Invoker()
print(f"Greeting from instance: {invoker_instance.greet('Diana')}")