class BookWithStrRepr:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"Book(title='{self.title}', author='{self.author}')"

    def __repr__(self):
        return f"<BookWithStrRepr title='{self.title}', author='{self.author}'>"

book_str_repr = BookWithStrRepr("The Shining", "Stephen King")
print(f"String representation: {str(book_str_repr)}")
print(f"Representation: {repr(book_str_repr)}")