import json

class Book:
    def __init__(self, title, author, year, genres):
        self.title = title
        self.author = author
        self.year = year
        self.genres = genres # List of strings

    def to_json(self):
        # json.dumps can serialize basic Python types (str, int, list, dict, bool, None)
        # We need to convert the object's attributes to a dictionary first.
        return json.dumps({
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genres": self.genres
        }, indent=4) # Using indent for pretty printing

# Create a Book object
book_instance = Book(
    title="The Hitchhiker's Guide to the Galaxy",
    author="Douglas Adams",
    year=1979,
    genres=["Science Fiction", "Comedy"]
)

# Get the JSON string representation
book_json_string = book_instance.to_json()

print("Book object serialized to JSON string:")
print(book_json_string)

# You could also save this to a file:
# with open("book_data.json", 'w') as f:
#     f.write(book_json_string)
# print("Book data saved to book_data.json")