big_list = list(range(1, 1000000))

# Check if any number is divisible by 99
if any(x % 99 == 0 for x in big_list):
    print("Found a number divisible by 99")
else:
    print("No number divisible by 99 found")