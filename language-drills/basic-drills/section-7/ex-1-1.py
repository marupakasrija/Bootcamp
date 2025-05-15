import timeit

execution_time = timeit.timeit('sum(range(10000))', number=1000)
print(f"Time taken to execute sum(range(10000)) 1000 times: {execution_time:.6f} seconds")