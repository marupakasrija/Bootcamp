def generate_numbers_yield(n):
    """Generates numbers up to n using yield."""
    for i in range(n):
        yield i

def get_numbers_return(n):
    """Returns a list of numbers up to n using return."""
    numbers = []
    for i in range(n):
        numbers.append(i)
    return numbers

if __name__ == "__main__":
    print("Using yield:")
    for num in generate_numbers_yield(5):
        print(num)

    print("\nUsing return:")
    numbers_list = get_numbers_return(5)
    for num in numbers_list:
        print(num)

# Explanation: The yield version produces items one at a time, making it memory-efficient
# for large sequences. The return version creates the entire list in memory before returning.