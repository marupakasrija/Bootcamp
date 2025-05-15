from collections import defaultdict

words = ["apple", "apricot", "banana", "bat", "cat", "car", "dog"]
grouped_words = defaultdict(list)

for word in words:
  first_letter = word[0]
  grouped_words[first_letter].append(word)

print("Words grouped by first letter:")
for letter, word_list in grouped_words.items():
  print(f"{letter}: {word_list}")

# Expected Output:
# Words grouped by first letter:
# a: ['apple', 'apricot']
# b: ['banana', 'bat']
# c: ['cat', 'car']
# d: ['dog']