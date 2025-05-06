def calculate_area(length, width, /, unit="units"):
    """Calculates the area. Length and width are positional-only."""
    area = length * width
    print(f"Area: {area} {unit}")

calculate_area(5, 10)             # Output: Area: 50 units
calculate_area(5, 10, "cm^2")      # Output: Area: 50 cm^2
try:
    calculate_area(length=5, width=10)
except TypeError as e:
    print(f"Error: {e}")
    # Output: Error: calculate_area() got some keyword-only arguments passed as positional arguments: 'length', 'width'