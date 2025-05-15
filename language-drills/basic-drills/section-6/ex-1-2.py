from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    country: str = "India"

if __name__ == "__main__":
    user1 = User("Alice", 30)
    user2 = User("Bob", 25, "USA")
    print(user1)
    print(user2)