class ParentWithClassMethod:
    @classmethod
    def factory(cls, data):
        return cls(data)

    def __init__(self, value):
        self.value = value

class ChildWithOverriddenFactory(ParentWithClassMethod):
    @classmethod
    def factory(cls, data):
        processed_data = f"Processed: {data}"
        return cls(processed_data)

parent_obj = ParentWithClassMethod.factory("Parent Data")
child_obj = ChildWithOverriddenFactory.factory("Child Data")

print(f"Parent object: {parent_obj.value}")
print(f"Child object: {child_obj.value}")