from dataclasses import dataclass

@dataclass
class UserDataclass:
    name: str
    age: int

user_dataclass = UserDataclass("Charlie", 30)
print(user_dataclass)