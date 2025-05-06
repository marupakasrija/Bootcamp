def prime_checker():
    value = yield None  # Initialize the generator
    while True:
        if value is not None:
            is_prime = True
            if value < 2:
                is_prime = False
            else:
                for i in range(2, int(value**0.5) + 1):
                    if value % i == 0:
                        is_prime = False
                        break
            yield f"{value} is prime: {is_prime}"
        else:
            value = yield "Send a number to check."

checker = prime_checker()
print(checker.send(None))  # Start the generator
print(checker.send(7))
print(checker.send(10))