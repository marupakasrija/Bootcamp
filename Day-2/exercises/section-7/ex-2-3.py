import csv

def filter_csv(filename, condition):
    """
    Filters a CSV file based on a given condition using a generator.

    Args:
        filename (str): The path to the CSV file.
        condition (callable): A function that takes a row (list) and returns True if the row should be included.

    Yields:
        list: A row from the CSV file that satisfies the condition.
    """
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Assuming the first row is the header
        yield header
        for row in reader:
            if condition(row):
                yield row

if __name__ == "__main__":
    # Create a dummy CSV file
    with open("data.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Value"])
        for i in range(10):
            writer.writerow([i, f"Item {i}", i * 2])

    def is_high_value(row):
        try:
            return int(row[2]) > 5
        except ValueError:
            return False

    for row in filter_csv("data.csv", is_high_value):
        print(row)