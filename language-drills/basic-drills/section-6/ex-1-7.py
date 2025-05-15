from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

if __name__ == "__main__":
    user1 = User("Alice", 30)
    user2 = User("Alice", 30)
    user3 = User("Bob", 25)
    print(f"user1 == user2: {user1 == user2}")
    print(f"user1 == user3: {user1 == user3}")