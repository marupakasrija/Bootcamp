from dataclasses import dataclass

@dataclass(slots=True)
class User:
    name: str
    age: int

if __name__ == "__main__":
    user1 = User("Alice", 30)
    print(user1)
    # Try to access a non-existent attribute (will raise AttributeError if slots are effective)
    # print(user1.__dict__)