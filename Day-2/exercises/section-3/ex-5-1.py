class UtilityClass:
    @staticmethod
    def is_valid_isbn_static(isbn):
        isbn = isbn.replace("-", "")
        if len(isbn) != 10 and len(isbn) != 13:
            return False
        if len(isbn) == 10:
            if not all(c.isdigit() for c in isbn[:-1]) or not (isbn[-1].isdigit() or isbn[-1] == 'X'):
                return False
            sum_val = sum((int(c) * (10 - i)) for i, c in enumerate(isbn[:-1]))
            check_digit = 10 - (sum_val % 11)
            if check_digit == 10:
                check_digit = 'X'
            return str(check_digit) == isbn[-1]
        elif len(isbn) == 13:
            if not all(c.isdigit() for c in isbn):
                return False
            sum_val = sum((int(c) * (3 if i % 2 != 0 else 1)) for i, c in enumerate(isbn))
            return sum_val % 10 == 0
        return False

print(f"Is '978-0321765723' valid? {UtilityClass.is_valid_isbn_static('978-0321765723')}")
