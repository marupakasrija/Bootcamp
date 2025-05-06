from collections import OrderedDict

od = OrderedDict()
od['apple'] = 1
od['banana'] = 2
od['cherry'] = 3
od['date'] = 4

print("Iterating over OrderedDict:")
for key, value in od.items():
  print(f"{key}: {value}")

# Demonstrate move_to_end
od.move_to_end('banana')
print("\nAfter moving 'banana' to end:")
for key, value in od.items():
  print(f"{key}: {value}")

# Expected Output:
# Iterating over OrderedDict:
# apple: 1
# banana: 2
# cherry: 3
# date: 4
#
# After moving 'banana' to end:
# apple: 1
# cherry: 3
# date: 4
# banana: 2