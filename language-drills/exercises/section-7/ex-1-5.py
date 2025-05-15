import timeit
import random

data = [random.randint(1, 100) for _ in range(10000)]

def custom_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

builtin_sort_time = timeit.timeit('sorted(data)', setup='from __main__ import data', number=10)
custom_sort_time = timeit.timeit('custom_sort(data)', setup='from __main__ import data, custom_sort; data = data[:] ', number=10)

print(f"Time taken for built-in sorted(): {builtin_sort_time:.6f} seconds")
print(f"Time taken for custom sort function: {custom_sort_time:.6f} seconds")