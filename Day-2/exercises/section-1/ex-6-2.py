class Counter:
    def __init__(self, n):
        self.n = n
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.n:
            result = self.current
            self.current += 1
            return result
        else:
            raise StopIteration

my_counter = Counter(5)
for i in my_counter:
    print(i)