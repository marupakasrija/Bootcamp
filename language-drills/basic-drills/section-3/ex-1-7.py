class Book:
    category = "Fiction"

    def __init__(self, title="Untitled", author="Unknown"):
        self.title = title
        self.author = author

    def describe(self):
        return f"'{self.title}' by {self.author} (Category: {self.category})"

    def update_title(self, new_title):
        self.title = new_title

book1 = Book("1984", "George Orwell")
book1.publication_year = 1949
print(f"Publication Year of '{book1.title}': {book1.publication_year}")