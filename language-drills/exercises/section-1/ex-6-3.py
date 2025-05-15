class ManualIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            value = self.data[self.index]
            self.index += 1
            return value
        else:
            raise StopIteration

my_data = [1, 2]
my_iter = ManualIterator(my_data)

try:
    print(next(my_iter))
    print(next(my_iter))
    print(next(my_iter))
except StopIteration:
    print("Iteration manually stopped.")