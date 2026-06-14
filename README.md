# OOP Part 2 – Cash Register Lab

A Python implementation of a cash register for an e-commerce site.  
Built as part of the Flatiron School OOP Phase 2 curriculum.

---

## Features

| Feature | Description |
|---|---|
| Add items | Add a product with price and optional quantity |
| Apply discount | Apply a percentage discount to the running total |
| Void last transaction | Remove the most recent item(s) and reverse their price |

---

## Project Structure

```
oop-p2-cash-register-lab/
├── lib/
│   ├── cash_register.py        # CashRegister class
│   └── test_cash_register.py  # Full pytest suite (33 tests)
├── pytest.ini
├── .gitignore
└── README.md
```

---

## CashRegister Class

### Attributes

| Attribute | Type | Description |
|---|---|---|
| `discount` | `int` | Percentage off the total (0–100) |
| `total` | `float` | Running price total |
| `items` | `list[str]` | Item names in the register |
| `previous_transactions` | `list[dict]` | Transaction history |

### Methods

#### `add_item(item, price, quantity=1)`
Adds one or more units of a product.
- Updates `total` by `price × quantity`
- Appends the item name to `items` once per unit
- Appends `{"item", "price", "quantity"}` to `previous_transactions`

#### `apply_discount()`
Applies the stored discount percentage to `total`.
- Resets `discount` to `0` after use so it cannot be double-applied
- Prints `"There is no discount to apply."` if no transactions exist

#### `void_last_transaction()`
Removes the last transaction and reverses its effect.
- Reduces `total` by the voided line's price
- Removes the corresponding item(s) from `items`
- Prints `"There is no transaction to void."` if history is empty

---

## Usage Example

```python
from lib.cash_register import CashRegister

# Create a register with a 20% discount
register = CashRegister(20)

# Add items
register.add_item("shirt", 30.00)          # total = 30.00
register.add_item("jeans", 50.00, 2)       # total = 130.00

print(register.items)
# ['shirt', 'jeans', 'jeans']

print(register.total)
# 130.0

# Apply the 20% discount
register.apply_discount()
print(register.total)   # 104.0

# Void the last transaction
register.void_last_transaction()
print(register.total)   # 54.0  (jeans ×2 = 100 removed from 104)
```

---

## Running Tests

```bash
pytest
```

All 33 tests should pass:

```
33 passed in 0.04s
```

---

## Git Workflow Used

```
main
 └── feature/cash-register   ← implementation + tests written here
      └── PR merged → main
```
