class MethodDifference:
    class_var = "I am a class variable"

    def __init__(self, instance_var):
        self.instance_var = instance_var

    @staticmethod
    def static_method_diff(x):
        print(f"Static method called with: {x}")
        # Cannot access self or cls here

    @classmethod
    def class_method_diff(cls, y):
        print(f"Class method called with: {y}")
        print(f"Accessing class variable: {cls.class_var}")
        # Can create an instance using cls
        instance = cls("created from class method")
        print(f"Instance created in class method: {instance.instance_var}")

diff_instance = MethodDifference("instance specific")
MethodDifference.static_method_diff(10)
MethodDifference.class_method_diff(20)