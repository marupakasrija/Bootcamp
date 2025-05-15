import itertools

color_pattern = ["red", "green", "blue"]
color_cycler = itertools.cycle(color_pattern)

print("Cycling through colors (6 items):")
for i in range(6):
  print(f"Item {i+1}: {next(color_cycler)}")

# Output:
# Item 1: red
# Item 2: green
# Item 3: blue
# Item 4: red
# Item 5: green
# Item 6: blue