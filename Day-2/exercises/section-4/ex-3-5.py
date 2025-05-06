import functools
import time

def fib_uncached(n):
  if n < 2:
    return n
  return fib_uncached(n-1) + fib_uncached(n-2)

@functools.lru_cache(maxsize=None)
def fib_cached(n):
  if n < 2:
    return n
  return fib_cached(n-1) + fib_cached(n-2)

# Test with a moderately large number where the difference will be apparent
n_val = 30 # Increasing this will show a much larger difference

start_time = time.perf_counter()
result_uncached = fib_uncached(n_val)
end_time = time.perf_counter()
time_uncached = end_time - start_time
print(f"Uncached Fibonacci({n_val}): {result_uncached}, Time: {time_uncached:.6f} seconds")

# Clear cache for a fair comparison if fib_cached was called before with n_val
# (though in this script it's the first call for this specific n_val)
# fib_cached.cache_clear() # if needed

start_time = time.perf_counter()
result_cached = fib_cached(n_val)
end_time = time.perf_counter()
time_cached = end_time - start_time
print(f"Cached Fibonacci({n_val}): {result_cached}, Time: {time_cached:.6f} seconds")

# Second call to cached version (should be extremely fast)
start_time = time.perf_counter()
result_cached_again = fib_cached(n_val)
end_time = time.perf_counter()
time_cached_again = end_time - start_time
print(f"Cached Fibonacci({n_val}) again: {result_cached_again}, Time: {time_cached_again:.8f} seconds")

# For n_val = 30:
# Uncached Fibonacci(30): 832040, Time: 0.2XXXXX seconds (will vary)
# Cached Fibonacci(30): 832040, Time: 0.000XXX seconds (first call, builds cache)
# Cached Fibonacci(30) again: 832040, Time: 0.00000XXX seconds (hits cache)
# The uncached version will become extremely slow for n > 35.