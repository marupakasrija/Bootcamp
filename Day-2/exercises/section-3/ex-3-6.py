class Book:
    category = "Fiction"

    def __init__(self, title="Untitled", author="Unknown"):
        self.title = title
        self.author = author

    def describe(self):
        return f"'{self.title}' by {self.author} (Category: {self.category})"

    def update_title(self, new_title):
        self.title = new_title
class LibraryWithGetitem:
    def __init__(self, books=None):
        self.books = books if books is not None else []

    def __getitem__(self, index):
        return self.books[index]

library_getitem = LibraryWithGetitem([Book("Romeo and Juliet", "Shakespeare"), Book("Othello", "Shakespeare")])
print(f"First book in library (using __getitem__): {library_getitem[0].title}")
