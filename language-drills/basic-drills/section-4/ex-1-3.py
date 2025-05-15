functions_list = [abs, str, hex]
value_to_apply = -42

results = []
for func in functions_list:
  results.append(func(value_to_apply))

print(f"Applying [abs, str, hex] to {value_to_apply}: {results}")
# Output: Applying [abs, str, hex] to -42: [42, '-42', '-0x2a']