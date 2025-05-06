from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    name: str
    age: int
    tags: List[str] = field(default_factory=list)

if __name__ == "__main__":
    user1 = User("Alice", 30)
    user2 = User("Bob", 25, ["coder", "reader"])
    print(user1)
    print(user2)
    user1.tags.append("learner")
    print(user1)