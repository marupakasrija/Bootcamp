def process_order(order_details):
    """Processes the given order details and returns the total cost."""
    items = order_details.get('items', [])
    shipping_address = order_details.get('shipping_address')
    total = 0
    for item in items:
        price = item.get('price', 0)
        quantity = item.get('quantity', 1)
        total += price * quantity

    if shipping_address and shipping_address.get('country') != "USA":
        total += 10  # International shipping fee

    return total

if __name__ == "__main__":
    order = {
        'items': [{'price': 20, 'quantity': 2}, {'price': 5, 'quantity': 4}],
        'shipping_address': {'country': 'Canada', 'city': 'Toronto'}
    }
    order_total = process_order(order)
    print(f"The total cost of the order is: ${order_total}")

# Avoid vague naming like:
# def process(data):
#     # ... uses 'data' for different things
#     temp = 0
#     for x in data:
#         temp += x['val']
#     if data['loc'] != "US":
#         temp += 10
#     return temp