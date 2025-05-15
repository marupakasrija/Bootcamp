class Book:
    category = "Fiction"

    def __init__(self, title="Untitled", author="Unknown"):
        self.title = title
        self.author = author

    def describe(self):
        return f"'{self.title}' by {self.author} (Category: {self.category})"

    def update_title(self, new_title):
        self.title = new_title
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

class BookManager:
    BOOK_FORMAT = "Title|Author"

    def __init__(self, books=None):
        self.books = books if books is not None else []

    def add_book(self, book):
        self.books.append(book)

    def list_titles(self):
        return [book.title for book in self.books]

    @classmethod
    def create_from_file(cls, filepath):
        books = []
        with open(filepath, 'r') as f:
            for line in f:
                title, author = line.strip().split("|")
                books.append(Book(title.strip(), author.strip()))
        return cls(books)

    @staticmethod
    def validate_book_string(book_string):
        parts = book_string.split("|")
        return len(parts) == 2 and all(part.strip() for part in parts)

# Example of Hybrid Usage
if BookManager.validate_book_string("The Alchemist|Paulo Coelho"):
    # Create a dummy books.txt
    with open("books.txt", "w") as f:
        f.write("The Alchemist|Paulo Coelho\n")
        f.write("The Great Gatsby|F. Scott Fitzgerald\n")
    manager = BookManager.create_from_file("books.txt")
    print(manager.list_titles())