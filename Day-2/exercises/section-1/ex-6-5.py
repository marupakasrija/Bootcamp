def running_total(numbers):
    current_total = 0
    for num in numbers:
        current_total += num
        yield current_total

data = [1, 2, 3, 4, 5]
for total in running_total(data):
    print(total)