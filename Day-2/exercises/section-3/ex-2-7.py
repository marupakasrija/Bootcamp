class Book:
    category = "Fiction"

    def __init__(self, title="Untitled", author="Unknown"):
        self.title = title
        self.author = author

    def describe(self):
        return f"'{self.title}' by {self.author} (Category: {self.category})"

    def update_title(self, new_title):
        self.title = new_title
class Novel(Book):
    def __init__(self, title, author, genre):
        super().__init__(title, author)
        self.genre = genre

    def describe(self):
        return f"Novel: {super().describe()} (Genre: {self.genre})"

    def __str__(self):
        return f"Book(title='{self.title}', author='{self.author}')"

novel1 = Novel("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "Science Fiction")
print(f"Is novel1 an instance of Novel? {isinstance(novel1, Novel)}")
print(f"Is novel1 an instance of Book? {isinstance(novel1, Book)}")