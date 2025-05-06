from dataclasses import dataclass
@dataclass(frozen=True)
class ImmutableUserDataclass:
    name: str
    age: int

immutable_user_dataclass = ImmutableUserDataclass("Eve", 25)
print(immutable_user_dataclass)
# Trying to modify immutable_user_dataclass.age = 31 would raise an error