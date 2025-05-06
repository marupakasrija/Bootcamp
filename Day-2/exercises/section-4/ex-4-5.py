import itertools

data_range = range(20) # 0, 1, ..., 19

# Skip first 3 (0, 1, 2), take next 4 (3, 4, 5, 6)
# itertools.islice(iterable, start, stop, step)
# If stop is None, it goes to the end.
# If only two args, it's (iterable, stop) which means start=0
# If three args, it's (iterable, start, stop)

# To skip 3 and take 4: start index is 3, stop index is 3+4 = 7
sliced_elements = list(itertools.islice(data_range, 3, 7))
print(f"Elements from range(20) after skipping 3 and taking 4: {sliced_elements}")
# Output: Elements from range(20) after skipping 3 and taking 4: [3, 4, 5, 6]

# Alternative: islice(iterable, start, stop, step) -> islice(iterable, 3, 3+4)
# or islice(iterable, start, None) to go to the end
# islice(iterable, stop) to take first `stop` elements.
# To "skip first 3 and take next 4":
# Start index for taking is 3.
# The 'stop' argument for islice is an exclusive upper bound index.
# So if we start at 3 and want 4 elements, we take indices 3, 4, 5, 6.
# This means stop = 7.
sliced_again = list(itertools.islice(data_range, 3, 3 + 4))
print(f"Using 3, 3+4: {sliced_again}")
# Output: Using 3, 3+4: [3, 4, 5, 6]

# If you had an infinite iterator, you'd use islice(iterator, start, stop)
# Example: take elements from index 3 up to (but not including) index 7
ids = itertools.count()
sliced_ids = list(itertools.islice(ids, 3, 7))
print(f"Sliced infinite IDs (indices 3-6): {sliced_ids}") # Output: [3, 4, 5, 6]
# The `ids` iterator is now advanced. next(ids) would yield 7.