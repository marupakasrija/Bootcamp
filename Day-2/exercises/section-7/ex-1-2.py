import timeit

list_comp_time = timeit.timeit('[x*x for x in range(1000000)]', number=10)
gen_expr_time = timeit.timeit('(x*x for x in range(1000000))', number=10)

print(f"Time taken for list comprehension: {list_comp_time:.6f} seconds")
print(f"Time taken for generator expression: {gen_expr_time:.6f} seconds")