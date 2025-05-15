class BookWithHash:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __eq__(self, other):
        if not isinstance(other, BookWithHash):
            return NotImplemented
        return self.title == other.title and self.author == other.author

    def __hash__(self):
        return hash((self.title, self.author))

book_hash_a = BookWithHash("Pride and Prejudice", "Jane Austen")
book_hash_b = BookWithHash("Pride and Prejudice", "Jane Austen")
book_hash_c = BookWithHash("Sense and Sensibility", "Jane Austen")

book_set_hash = {book_hash_a, book_hash_b, book_hash_c}
print(f"Set of books (with hashing): {book_set_hash}")