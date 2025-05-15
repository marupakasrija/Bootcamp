class Book:
    category = "Fiction"

    def __init__(self, title="Untitled", author="Unknown"):
        self.title = title
        self.author = author

    def describe(self):
        return f"'{self.title}' by {self.author} (Category: {self.category})"

    def update_title(self, new_title):
        self.title = new_title

book2 = Book()
print(f"Book 2 - Title: {book2.title}, Author: {book2.author}")
book3 = Book("Brave New World")
print(f"Book 3 - Title: {book3.title}, Author: {book3.author}")