class BookWithEquality:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __eq__(self, other):
        if not isinstance(other, BookWithEquality):
            return NotImplemented
        return self.title == other.title and self.author == other.author

book_eq_a = BookWithEquality("The Lord of the Rings", "J.R.R. Tolkien")
book_eq_b = BookWithEquality("The Lord of the Rings", "J.R.R. Tolkien")
book_eq_c = BookWithEquality("The Hobbit", "J.R.R. Tolkien")

print(f"book_eq_a == book_eq_b: {book_eq_a == book_eq_b}")
print(f"book_eq_a == book_eq_c: {book_eq_a == book_eq_c}")