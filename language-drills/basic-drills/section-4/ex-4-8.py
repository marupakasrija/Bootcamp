import itertools

my_list = [1, 2, 3]

# Combinations: Order does not matter, no repeated elements.
# Pairs (combinations of length 2)
pairs_combinations = list(itertools.combinations(my_list, 2))
print(f"Combinations (pairs) from {my_list}: {pairs_combinations}")
# Output: Combinations (pairs) from [1, 2, 3]: [(1, 2), (1, 3), (2, 3)]

# Triples (combinations of length 3)
triples_combinations = list(itertools.combinations(my_list, 3))
print(f"Combinations (triples) from {my_list}: {triples_combinations}")
# Output: Combinations (triples) from [1, 2, 3]: [(1, 2, 3)]


# Permutations: Order matters, no repeated elements by default.
# Pairs (permutations of length 2)
pairs_permutations = list(itertools.permutations(my_list, 2))
print(f"\nPermutations (pairs) from {my_list}: {pairs_permutations}")
# Output: Permutations (pairs) from [1, 2, 3]: [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]

# Triples (permutations of length 3)
# If r (length) is not specified or is None, then r defaults to the length of the iterable
# and all full-length permutations are generated.
triples_permutations = list(itertools.permutations(my_list, 3))
print(f"Permutations (triples) from {my_list}: {triples_permutations}")
# Output: Permutations (triples) from [1, 2, 3]: [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]

# If you want combinations/permutations *with replacement*:
# combinations_with_replacement
pairs_combs_wr = list(itertools.combinations_with_replacement(my_list, 2))
print(f"\nCombinations with replacement (pairs) from {my_list}: {pairs_combs_wr}")
# Output: [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]

# product (for permutations with replacement, or Cartesian product)
# If you want all possible pairs where elements can be repeated and order matters, use product
# For example, to simulate drawing two items from [1,2,3] with replacement, where (1,2) is different from (2,1)
# and (1,1) is possible.
product_pairs = list(itertools.product(my_list, repeat=2))
print(f"Product (like permutations with replacement, pairs) from {my_list}: {product_pairs}")
# Output: [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]