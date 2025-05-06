import itertools
from operator import itemgetter

data = [
    {'city': 'New York', 'name': 'Alice', 'role': 'Engineer'},
    {'city': 'London', 'name': 'Bob', 'role': 'Designer'},
    {'city': 'New York', 'name': 'Charlie', 'role': 'Engineer'},
    {'city': 'Paris', 'name': 'Diana', 'role': 'Manager'},
    {'city': 'London', 'name': 'Eve', 'role': 'Engineer'},
    {'city': 'New York', 'name': 'Frank', 'role': 'Designer'},
]

# For groupby to work correctly, the data must be sorted by the grouping key.
# Let's group by 'city'
data_sorted_by_city = sorted(data, key=itemgetter('city'))

print("Grouping by 'city':")
for key, group in itertools.groupby(data_sorted_by_city, key=itemgetter('city')):
    print(f"\nCity: {key}")
    for item in group:
        print(f"  - {item['name']} ({item['role']})")

# Output:
# Grouping by 'city':

# City: London
#   - Bob (Designer)
#   - Eve (Engineer)

# City: New York
#   - Alice (Engineer)
#   - Charlie (Engineer)
#   - Frank (Designer)

# City: Paris
#   - Diana (Manager)

print("\n--- Grouping by 'role' ---")
# Now group by 'role'
data_sorted_by_role = sorted(data, key=itemgetter('role'))
for key, group in itertools.groupby(data_sorted_by_role, key=itemgetter('role')):
    print(f"\nRole: {key}")
    # The group is an iterator, so convert to list if you need to reuse or print nicely
    group_list = list(group)
    print(f"  Count: {len(group_list)}")
    for item in group_list:
        print(f"  - {item['name']} from {item['city']}")

# Output:
# --- Grouping by 'role' ---

# Role: Designer
#   Count: 2
#   - Bob from London
#   - Frank from New York

# Role: Engineer
#   Count: 3
#   - Alice from New York
#   - Charlie from New York
#   - Eve from London

# Role: Manager
#   Count: 1
#   - Diana from Paris