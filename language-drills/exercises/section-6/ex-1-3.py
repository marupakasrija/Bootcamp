from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    country: str = "India"

    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age cannot be negative")

if __name__ == "__main__":
    try:
        user1 = User("Alice", -5)
    except ValueError as e:
        print(f"Error creating user: {e}")

    user2 = User("Bob", 30)
    print(user2)