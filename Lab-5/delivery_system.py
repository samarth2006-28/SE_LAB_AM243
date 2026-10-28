"""Order queue manager for a food delivery kitchen."""

import json
from datetime import datetime

# Global state
orders = {}
menu = {}
VALID_STATUSES = ["placed", "cooking", "out_for_delivery", "delivered"]
DEFAULT_MENU = {"pizza": 250, "burger": 150, "fries": 90, "coke": 40}

def create_order(customer, items, order_history=None):
    """Create an order priced from the menu and return its id."""
    if not customer:
        raise ValueError("Order needs a customer name")
    if not items:
        raise ValueError("Order needs at least one item")
    unknown = [i for i in items if i not in menu]
    if unknown:
        raise ValueError(f"Unknown dishes: {', '.join(unknown)}")
    if order_history is None:
        order_history = []
    order_id = max(orders, default=0) + 1
    total = sum(menu[i] for i in items)
    orders[order_id] = {"customer": customer, "items": items, "total": total, "status": "placed"}
    order_history.append(order_id)
    return order_id

def update_order_status(order_id, status):
    """Set an order's status; return False if the order or status is invalid."""
    if status not in VALID_STATUSES:
        print(f"Invalid status {status!r} for order {order_id}")
        return False
    if order_id not in orders:
        print(f"Order {order_id} not found")
        return False
    orders[order_id]["status"] = status
    return True

def read_menu_config(file="menu.json"):
    """Load the menu from a JSON file, falling back to the default menu."""
    menu.clear()
    try:
        with open(file, encoding="utf-8") as f:
            menu.update(json.load(f))
    except (OSError, json.JSONDecodeError):
        menu.update(DEFAULT_MENU)

def daily_revenue():
    """Return the total value of all delivered orders."""
    return sum(o["total"] for o in orders.values() if o["status"] == "delivered")

def backup_orders(file="orders.json"):
    """Write all orders to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(orders, f)

def restore_orders(file="orders.json"):
    """Replace the current orders with those saved in a JSON file."""
    with open(file, encoding="utf-8") as f:
        data = json.load(f)
    orders.clear()
    # JSON object keys are always strings, so turn order ids back into ints
    orders.update({int(k): v for k, v in data.items()})

def print_queue():
    """Print every order with its customer, status and total."""
    print(f"Order queue at {datetime.now()}")
    for order_id, o in orders.items():
        print(order_id, o["customer"], o["status"], o["total"])

def main():
    """Run a sample day of orders."""
    read_menu_config()
    a = create_order("Asha", ["pizza", "coke"])
    for customer, items in [("Ravi", ["burger", "sushi"]), ("", [])]:
        try:
            create_order(customer, items)
        except ValueError as e:
            print(f"Order rejected: {e}")
    b = create_order("Ravi", ["burger", "fries"])
    update_order_status(a, "delivered")
    update_order_status(b, "teleported")
    update_order_status(42, "delivered")
    update_order_status(b, "out_for_delivery")
    print("Revenue today:", daily_revenue())
    backup_orders()
    restore_orders()
    print_queue()

if __name__ == "__main__":
    main()
