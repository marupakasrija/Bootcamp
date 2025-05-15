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
class BookAlternativeConstructors:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def describe(self):
        return f"'{self.title}' by {self.author}"

    @classmethod
    def from_string_alt(cls, s):
        title, author = s.split("|")
        return cls(title.strip(), author.strip())

    @classmethod
    def from_dict_alt(cls, data):
        return cls(data.get("title"), data.get("author"))

book_from_string_alt = BookAlternativeConstructors.from_string_alt("Foundation|Isaac Asimov")
print(book_from_string_alt.describe())

book_from_dict_alt = BookAlternativeConstructors.from_dict_alt({"title": "The Caves of Steel", "author": "Isaac Asimov"})
print(book_from_dict_alt.describe())