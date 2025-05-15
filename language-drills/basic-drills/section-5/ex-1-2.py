from collections import Counter

text = "hello world"
char_counts = Counter(text)

print(f"Character frequencies in '{text}':")
print(char_counts)

# Expected Output:
# Character frequencies in 'hello world':
# Counter({'l': 3, 'o': 2, 'h': 1, 'e': 1, ' ': 1, 'w': 1, 'r': 1, 'd': 1})