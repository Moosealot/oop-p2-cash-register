import pytest
from cash_register import CashRegister


# ======================================================================
# __init__ / attribute initialisation
# ======================================================================

class TestInit:
    def test_default_discount_is_zero(self):
        cr = CashRegister()
        assert cr.discount == 0

    def test_custom_discount_stored(self):
        cr = CashRegister(20)
        assert cr.discount == 20

    def test_total_initialised_to_zero(self):
        cr = CashRegister()
        assert cr.total == 0

    def test_items_initialised_as_empty_list(self):
        cr = CashRegister()
        assert cr.items == []

    def test_previous_transactions_initialised_as_empty_list(self):
        cr = CashRegister()
        assert cr.previous_transactions == []


# ======================================================================
# discount property validation
# ======================================================================

class TestDiscountProperty:
    def test_valid_discount_lower_bound(self):
        cr = CashRegister(0)
        assert cr.discount == 0

    def test_valid_discount_upper_bound(self):
        cr = CashRegister(100)
        assert cr.discount == 100

    def test_valid_discount_midrange(self):
        cr = CashRegister(50)
        assert cr.discount == 50

    def test_negative_discount_rejected(self, capsys):
        cr = CashRegister(-5)
        captured = capsys.readouterr()
        assert "Not valid discount" in captured.out
        assert cr.discount == 0

    def test_discount_above_100_rejected(self, capsys):
        cr = CashRegister(101)
        captured = capsys.readouterr()
        assert "Not valid discount" in captured.out
        assert cr.discount == 0

    def test_float_discount_rejected(self, capsys):
        cr = CashRegister(10.5)
        captured = capsys.readouterr()
        assert "Not valid discount" in captured.out
        assert cr.discount == 0

    def test_string_discount_rejected(self, capsys):
        cr = CashRegister("ten")
        captured = capsys.readouterr()
        assert "Not valid discount" in captured.out
        assert cr.discount == 0

    def test_setter_updates_discount(self):
        cr = CashRegister()
        cr.discount = 30
        assert cr.discount == 30


# ======================================================================
# add_item
# ======================================================================

class TestAddItem:
    def test_add_item_updates_total(self):
        cr = CashRegister()
        cr.add_item("apple", 1.50)
        assert cr.total == 1.50

    def test_add_item_default_quantity_one(self):
        cr = CashRegister()
        cr.add_item("banana", 0.75)
        assert cr.items.count("banana") == 1

    def test_add_item_with_quantity(self):
        cr = CashRegister()
        cr.add_item("mango", 2.00, 3)
        assert cr.total == 6.00
        assert cr.items.count("mango") == 3

    def test_add_item_appends_to_items(self):
        cr = CashRegister()
        cr.add_item("shirt", 20.00)
        assert "shirt" in cr.items

    def test_add_item_records_transaction(self):
        cr = CashRegister()
        cr.add_item("hat", 15.00, 2)
        assert len(cr.previous_transactions) == 1
        txn = cr.previous_transactions[0]
        assert txn["item"] == "hat"
        assert txn["price"] == 30.00
        assert txn["quantity"] == 2

    def test_multiple_add_items_accumulate_total(self):
        cr = CashRegister()
        cr.add_item("pen", 1.00)
        cr.add_item("notebook", 5.00)
        assert cr.total == 6.00

    def test_multiple_add_items_accumulate_transactions(self):
        cr = CashRegister()
        cr.add_item("pen", 1.00)
        cr.add_item("notebook", 5.00)
        assert len(cr.previous_transactions) == 2


# ======================================================================
# apply_discount
# ======================================================================

class TestApplyDiscount:
    def test_apply_discount_reduces_total(self):
        cr = CashRegister(20)
        cr.add_item("jeans", 100.00)
        cr.apply_discount()
        assert cr.total == 80.00

    def test_apply_discount_resets_discount_to_zero(self):
        cr = CashRegister(10)
        cr.add_item("shoes", 50.00)
        cr.apply_discount()
        assert cr.discount == 0

    def test_apply_discount_cannot_be_applied_twice(self):
        cr = CashRegister(10)
        cr.add_item("shoes", 50.00)
        cr.apply_discount()
        total_after_first = cr.total
        cr.apply_discount()          # second call — discount is now 0
        assert cr.total == total_after_first

    def test_apply_discount_with_no_transactions_prints_message(self, capsys):
        cr = CashRegister(15)
        cr.apply_discount()
        captured = capsys.readouterr()
        assert "There is no discount to apply." in captured.out

    def test_apply_discount_does_not_change_items(self):
        cr = CashRegister(25)
        cr.add_item("coat", 200.00)
        cr.apply_discount()
        assert "coat" in cr.items

    def test_apply_zero_discount_leaves_total_unchanged(self):
        cr = CashRegister(0)
        cr.add_item("socks", 5.00)
        cr.apply_discount()
        assert cr.total == 5.00


# ======================================================================
# void_last_transaction
# ======================================================================

class TestVoidLastTransaction:
    def test_void_removes_last_transaction(self):
        cr = CashRegister()
        cr.add_item("book", 10.00)
        cr.void_last_transaction()
        assert len(cr.previous_transactions) == 0

    def test_void_reduces_total(self):
        cr = CashRegister()
        cr.add_item("book", 10.00)
        cr.void_last_transaction()
        assert cr.total == 0.00

    def test_void_removes_item_from_items(self):
        cr = CashRegister()
        cr.add_item("lamp", 25.00)
        cr.void_last_transaction()
        assert "lamp" not in cr.items

    def test_void_multi_quantity_removes_all_units(self):
        cr = CashRegister()
        cr.add_item("pen", 1.00, 5)
        cr.void_last_transaction()
        assert cr.items.count("pen") == 0
        assert cr.total == 0.00

    def test_void_only_removes_last_transaction(self):
        cr = CashRegister()
        cr.add_item("apple", 1.00)
        cr.add_item("orange", 2.00)
        cr.void_last_transaction()
        assert cr.total == 1.00
        assert "apple" in cr.items
        assert "orange" not in cr.items

    def test_void_with_no_transactions_prints_message(self, capsys):
        cr = CashRegister()
        cr.void_last_transaction()
        captured = capsys.readouterr()
        assert "There is no transaction to void." in captured.out

    def test_void_twice_removes_two_transactions(self):
        cr = CashRegister()
        cr.add_item("a", 1.00)
        cr.add_item("b", 2.00)
        cr.void_last_transaction()
        cr.void_last_transaction()
        assert cr.total == 0.00
        assert cr.items == []
