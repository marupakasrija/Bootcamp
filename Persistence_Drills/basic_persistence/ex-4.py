import json

class Book:
    def __init__(self, title, author, year, genres):
        self.title = title
        self.author = author
        self.year = year
        self.genres = genres

    def to_json(self):
         return json.dumps({
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genres": self.genres
        }, indent=4)

    @classmethod
    def from_json(cls, json_string):
        # json.loads converts a JSON string back into a Python dictionary
        data = json.loads(json_string)
        # We use the dictionary to create a new Book instance
        return cls(
            title=data.get("title"), # Use .get() to avoid KeyError if a key is missing
            author=data.get("author"),
            year=data.get("year"),
            genres=data.get("genres", []) # Provide a default empty list for genres
        )

# Example JSON string (could be read from a file)
book_json_string = """
{
    "title": "1984",
    "author": "George Orwell",
    "year": 1949,
    "genres": ["Dystopian", "Science Fiction"]
}
"""

# Create a Book object from the JSON string using the class method
loaded_book = Book.from_json(book_json_string)

print("Book object deserialized from JSON string:")
print(f"Title: {loaded_book.title}")
print(f"Author: {loaded_book.author}")
print(f"Year: {loaded_book.year}")
print(f"Genres: {loaded_book.genres}")

# Example of reading from a file (assuming book_data.json exists)
# try:
#     with open("book_data.json", 'r') as f:
#         file_json_string = f.read()
#     loaded_book_from_file = Book.from_json(file_json_string)
#     print("\nBook object deserialized from file:")
#     print(f"Title: {loaded_book_from_file.title}")
# except FileNotFoundError:
#     print("\nbook_data.json not found. Skipping file deserialization example.")