class DynamicAttributes:
    def __init__(self, data):
        self._data = data

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

obj = DynamicAttributes({"x": 10, "y": 20})
print(obj.x)
print(obj.y)
try:
    print(obj.z)
except AttributeError as e:
    print(e)