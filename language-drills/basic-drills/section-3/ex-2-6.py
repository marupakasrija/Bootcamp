class Book:
    category = "Fiction"

    def __init__(self, title="Untitled", author="Unknown"):
        self.title = title
        self.author = author

    def describe(self):
        return f"'{self.title}' by {self.author} (Category: {self.category})"

    def update_title(self, new_title):
        self.title = new_title

class AudioMixin:
    def play(self):
        print("Playing audio...")

class AudioBook(Book, AudioMixin):
    def __init__(self, title, author, narrator):
        super().__init__(title, author)
        self.narrator = narrator

    def describe(self):
        return f"Audiobook: '{self.title}' by {self.author}, narrated by {self.narrator}"

audio_book = AudioBook("Foundation", "Isaac Asimov", "David Silver")
print(audio_book.describe())
audio_book.play()