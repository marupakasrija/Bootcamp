# 04_json_deserialize.py
import json

# The class definition must be available
class Book:
    def __init__(self, title, author, year, genre=None):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def from_dict(cls, data):
         """Creates a Book instance from a dictionary."""
         if isinstance(data, dict) and 'title' in data and 'author' in data and 'year' in data:
              return cls(
                  title=data['title'],
                  author=data['author'],
                  year=data['year'],
                  genre=data.get('genre') # Use .get() for optional keys
              )
         else:
             raise ValueError("Invalid data structure for Book deserialization.")

    @classmethod
    def from_json(cls, json_string):
        """Creates a Book instance from a JSON string."""
        try:
            data = json.loads(json_string)
            return cls.from_dict(data)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON string: {e}")
            return None
        except ValueError as e:
            print(f"Error creating Book object from JSON: {e}")
            return None
        except Exception as e:
             print(f"An unexpected error occurred during deserialization: {e}")
             return None


# Example JSON string (or load from book_data.json created by 03)
json_file = "book_data.json"
book_json_string = None
try:
    with open(json_file, 'r') as f:
        book_json_string = f.read()
    print(f"Read JSON string from {json_file}")
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file}. Please run 03_json_serialize.py first.")
except Exception as e:
    print(f"Error reading JSON file: {e}")


# Deserialize the JSON string back into a Book object
loaded_book = None
if book_json_string:
    loaded_book = Book.from_json(book_json_string)

if loaded_book:
    print("\nSuccessfully deserialized JSON string into a Book object:")
    print(f"Title: {loaded_book.title}")
    print(f"Author: {loaded_book.author}")
    print(f"Year: {loaded_book.year}")
    print(f"Genre: {loaded_book.genre}")
    print(f"Type of loaded object: {type(loaded_book)}")
else:
    print("\nFailed to deserialize JSON string.")