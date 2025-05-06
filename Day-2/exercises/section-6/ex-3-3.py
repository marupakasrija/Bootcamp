from typing import Optional
from pydantic import BaseModel, Field

class Item(BaseModel):
    """A simple item with a name and price."""
    name: str = Field(..., title="Item Name", description="The name of the item")
    price: float = Field(..., title="Price", description="The price of the item", example=9.99)

if __name__ == "__main__":
    item = Item(name="Laptop", price=1200.50)
    print(item.schema_json(indent=2))