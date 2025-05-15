def is_eligible_for_discount(customer_type, purchase_amount):
    """Checks if a customer is eligible for a discount."""
    return customer_type == "premium" and purchase_amount > 100

def apply_discount(purchase_amount):
    """Applies a 10% discount to the purchase amount."""
    return purchase_amount * 0.9

def calculate_final_price(customer_type, purchase_amount):
    """Calculates the final price after applying a discount if eligible."""
    if is_eligible_for_discount(customer_type, purchase_amount):
        return apply_discount(purchase_amount)
    else:
        return purchase_amount

if __name__ == "__main__":
    final_price = calculate_final_price("premium", 150)
    print(f"Final price for premium customer with $150 purchase: ${final_price}")

    final_price = calculate_final_price("regular", 120)
    print(f"Final price for regular customer with $120 purchase: ${final_price}")

# Original nested structure:
# def calculate_price(type, amount):
#     if type == "premium":
#         if amount > 100:
#             return amount * 0.9
#         else:
#             return amount
#     else:
#         return amount