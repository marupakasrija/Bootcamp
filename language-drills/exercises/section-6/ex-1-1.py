from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

if __name__ == "__main__":
    user1 = User("Alice", 30)
    print(user1)