class CashRegister:

    def __init__(self, discount=0):

        self.discount = discount
        self.total = 0
        self.items = []
        self.previous_transactions = []

    @property
    def discount(self):
        """int: Percentage discount (0–100)."""
        return self._discount

    @discount.setter
    def discount(self, value):
        if not isinstance(value, int) or not (0 <= value <= 100):
            print("Not valid discount")
            self._discount = 0
        else:
            self._discount = value

    def add_item(self, item, price, quantity=1):

        line_total = price * quantity
        self.total += line_total

        self.items.extend([item] * quantity)

        self.previous_transactions.append(
            {"item": item, "price": line_total, "quantity": quantity}
        )

    def apply_discount(self):
        if not self.previous_transactions:
            print("There is no discount to apply.")
            return

        # Calculate and apply the discount to the total.
        discount_amount = self.total * (self._discount / 100)
        self.total -= discount_amount

        # Reset discount so it cannot be applied again.
        self._discount = 0

    def void_last_transaction(self):

        if not self.previous_transactions:
            print("There is no transaction to void.")
            return

        last = self.previous_transactions.pop()

        # Reverse the price impact.
        self.total -= last["price"]

        # Remove items — pop from the end for each unit in the voided line.
        for _ in range(last["quantity"]):
            if self.items:
                self.items.pop()
