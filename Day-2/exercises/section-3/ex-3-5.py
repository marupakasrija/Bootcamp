class LibraryWithLen:
    def __init__(self, books=None):
        self.books = books if books is not None else []

    def __len__(self):
        return len(self.books)

class Book:
    category = "Fiction"

    def __init__(self, title="Untitled", author="Unknown"):
        self.title = title
        self.author = author

    def describe(self):
        return f"'{self.title}' by {self.author} (Category: {self.category})"

    def update_title(self, new_title):
        self.title = new_title

library_len = LibraryWithLen([Book("Hamlet", "Shakespeare"), Book("Macbeth", "Shakespeare")])
print(f"Number of books in library (using __len__): {len(library_len)}")