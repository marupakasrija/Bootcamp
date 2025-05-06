from collections import deque

d = deque([1, 2, 3, 4, 5])
print(f"Original deque: {d}")

# Rotate right by 2 positions
d.rotate(2)
print(f"Deque rotated right by 2: {d}") # Output: deque([4, 5, 1, 2, 3])

# Rotate left by 2 positions (is rotate(-2))
d = deque([1, 2, 3, 4, 5]) # Reset
d.rotate(-2)
print(f"Deque rotated left by 2: {d}") # Output: deque([3, 4, 5, 1, 2])