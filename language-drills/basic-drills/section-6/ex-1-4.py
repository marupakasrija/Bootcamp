from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    name: str
    age: int

if __name__ == "__main__":
    user1 = User("Alice", 30)
    print(user1)
    # The following line will cause an error
    # user1.age = 31