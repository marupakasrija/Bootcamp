class BookWithOrdering:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __lt__(self, other):
        return self.title < other.title

books_sort = [BookWithOrdering("Catcher in the Rye", "J.D. Salinger"),
               BookWithOrdering("To Kill a Mockingbird", "Harper Lee")]
books_sort.sort()
for book in books_sort:
    print(f"Sorted book: {book.title}")