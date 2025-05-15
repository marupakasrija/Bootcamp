from pydantic import BaseModel

class Product(BaseModel):
    """Represents a product with a name and a cost."""
    name: str
    cost: float

if __name__ == "__main__":
    product = Product(name="Book", cost=25.00)
    print(product)
    print(Product.__doc__)