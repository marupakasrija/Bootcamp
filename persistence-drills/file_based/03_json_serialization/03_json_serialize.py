# 03_json_serialize.py
import json

class Book:
    def __init__(self, title, author, year, genre=None):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def to_dict(self):
        """Converts the Book object to a dictionary suitable for JSON serialization."""
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre
        }

    def to_json(self):
        """Returns the JSON string representation of the Book object."""
        # The default JSONEncoder doesn't know how to serialize custom objects directly.
        # Convert the object to a dictionary first.
        return json.dumps(self.to_dict(), indent=4) # Use indent for pretty printing

# Create a Book instance
book1 = Book(title="The Hitchhiker's Guide to the Galaxy", author="Douglas Adams", year=1979, genre="Science Fiction")

# Get the JSON string
book_json_string = book1.to_json()

print("Book object serialized to JSON string:")
print(book_json_string)

# You can also serialize directly to a file
json_file = "book_data.json"
try:
    with open(json_file, 'w') as f:
        json.dump(book1.to_dict(), f, indent=4)
    print(f"\nSerialized Book object to {json_file}")
except Exception as e:
    print(f"Error during JSON file serialization: {e}")