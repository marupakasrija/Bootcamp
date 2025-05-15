class InventoryBool:
    def __init__(self, items=None):
        self.items = items if items is not None else []

    def __bool__(self):
        return bool(self.items)

inventory_bool1 = InventoryBool()
inventory_bool2 = InventoryBool(["pen", "paper"])

print(f"Is inventory_bool1 True? {bool(inventory_bool1)}")
print(f"Is inventory_bool2 True? {bool(inventory_bool2)}")