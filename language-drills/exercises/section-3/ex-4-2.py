from dataclasses import dataclass
@dataclass
class UserDataclassDefault:
    name: str
    age: int = 0

user_default = UserDataclassDefault("Diana")
print(user_default)