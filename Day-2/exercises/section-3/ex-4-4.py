from dataclasses import dataclass
@dataclass
class UserDataclass:
    name: str
    age: int

user_compare1 = UserDataclass("Charlie", 30)
user_compare2 = UserDataclass("Charlie", 30)
print(f"user_compare1 == user_compare2: {user_compare1 == user_compare2}")