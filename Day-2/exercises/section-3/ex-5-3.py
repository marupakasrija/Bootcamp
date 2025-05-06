class BookWithClassMethod:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def describe(self):
        return f"'{self.title}' by {self.author}"

    @classmethod
    def from_string_classmethod(cls, s):
        title, author = s.split("|")
        return cls(title.strip(), author.strip())
class NovelSubclassMethod(BookWithClassMethod):
    def __init__(self, title, author, genre):
        super().__init__(title, author)
        self.genre = genre

    def describe(self):
        return f"Novel: {super().describe()} (Genre: {self.genre})"

    @classmethod
    def from_string_classmethod(cls, s):
        title, author, genre = s.split("|")
        return cls(title.strip(), author.strip(), genre.strip())

novel_classmethod = NovelSubclassMethod.from_string_classmethod("Dune|Frank Herbert|Science Fiction")
print(novel_classmethod.describe())