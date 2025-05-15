from dataclasses import dataclass
@dataclass
class UserDataclassMethod:
    name: str
    age: int

    def is_adult(self):
        return self.age >= 18

user_method1 = UserDataclassMethod("Frank", 15)
print(f"{user_method1.name} is adult? {user_method1.is_adult()}")