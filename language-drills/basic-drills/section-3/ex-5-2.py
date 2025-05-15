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

book_classmethod = BookWithClassMethod.from_string_classmethod("The Martian|Andy Weir")
print(book_classmethod.describe())