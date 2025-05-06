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
book1.update_title("Nineteen Eighty-Four")
print(f"Updated Title: {book1.title}")