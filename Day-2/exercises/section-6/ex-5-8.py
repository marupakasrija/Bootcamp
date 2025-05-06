def calculate_tax(price, tax_rate):
    """
    Calculates the tax amount for a given price.

    Args:
        price (float): The original price of the item.
        tax_rate (float): The tax rate as a decimal (e.g., 0.05 for 5%).

    Returns:
        float: The calculated tax amount.
    """
    tax_amount = price * tax_rate  # Calculate the tax by multiplying price and tax rate
    return tax_amount

if __name__ == "__main__":
    item_price = 100.00
    sales_tax_rate = 0.07
    tax = calculate_tax(item_price, sales_tax_rate)
    print(f"The tax amount for an item priced at ${item_price} is: ${tax:.2f}")

# Instead of:
# def calculate_tax(p, tr):
#     # multiply price by tax rate
#     ta = p * tr
#     return ta