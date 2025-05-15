import pdb

def calculate_average(numbers):
    total = sum(numbers)
    pdb.set_trace()  # Execution will pause here
    count = len(numbers)
    if count == 0:
        return 0
    average = total / count
    return average

if __name__ == "__main__":
    data = [1, 2, 3, 4, 5]
    avg = calculate_average(data)
    print(f"The average is: {avg}")