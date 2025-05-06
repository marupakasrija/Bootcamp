from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int

    def is_adult(self):
        return self.age >= 18

if __name__ == "__main__":
    user1 = User("Alice", 15)
    user2 = User("Bob", 22)
    print(f"{user1.name} is an adult: {user1.is_adult()}")
    print(f"{user2.name} is an adult: {user2.is_adult()}")