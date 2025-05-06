from dataclasses import dataclass
@dataclass
class UserDataclass:
    name: str
    age: int
@dataclass
class AdminUserDataclass(UserDataclass):
    access_level: str

admin_user_dataclass = AdminUserDataclass("Heidi", 40, "admin")
print(admin_user_dataclass)
