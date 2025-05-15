import functools

@functools.lru_cache(maxsize=None) # maxsize=None for unlimited cache
def fib(n):
  if n < 0:
    raise ValueError("Input must be a non-negative integer")
  if n < 2:
    # print(f"fib({n}) -> base case")
    return n
  # print(f"fib({n}) -> calling fib({n-1}) + fib({n-2})")
  return fib(n-1) + fib(n-2)

# To see the caching effect, you'd typically print inside or compare performance.
# The lru_cache will store results of fib(k) and reuse them.
print(f"fib(10): {fib(10)}") # Output: 55
# Call again, it will be much faster and use cached values
print(f"fib(10) again: {fib(10)}") # Output: 55
print(f"fib(20): {fib(20)}") # Output: 6765

# Show cache info
print(f"Cache info for fib: {fib.cache_info()}")
# Output: Cache info for fib: CacheInfo(hits=..., misses=..., maxsize=None, currsize=...)