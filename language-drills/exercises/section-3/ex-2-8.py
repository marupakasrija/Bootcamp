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
class AudioMixin:
    def play(self):
        print("Playing audio...")

class AudioBook(Book, AudioMixin):
    def __init__(self, title, author, narrator):
        super().__init__(title, author)
        self.narrator = narrator

    def describe(self):
        return f"Audiobook: '{self.title}' by {self.author}, narrated by {self.narrator}"


book1 = Book("1984", "George Orwell")
novel1 = Novel("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "Science Fiction")
audio_book = AudioBook("Foundation", "Isaac Asimov", "David Silver")
books = [book1, novel1, audio_book]
for book in books:
    print(book.describe())