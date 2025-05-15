def outer_counter():
    count = 0
    def inner_increment():
        nonlocal count
        count += 1
        print(f"Inner count: {count}")
    inner_increment()
    print(f"Outer count: {count}")

outer_counter()