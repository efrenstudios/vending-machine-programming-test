# test_vending_machine.py
import unittest
import vending_machine 


class VendingMachineTests(unittest.TestCase):
    def setUp(self):
        # Start with known inventory and coins; reset order and balance
        vending_machine.set_inventory({"still": 5, "fizzy": 5}, {1: 50, 2: 20, 5: 10, 10: 10},)
        vending_machine.current_order_index = 0    # first in selling_order is "fizzy"
        vending_machine.inserted_total = 0

    def test_buy_fizzy_exact_no_change(self):
        vending_machine.insert_coin(10)
        vending_machine.insert_coin(10)
        vending_machine.insert_coin(10)
        vending_machine.insert_coin(5)  # total 35
        message = vending_machine.purchase_water("fizzy")
        self.assertIn("Dispensed: Fizzy Water", message)
        self.assertIn("Change $0", message)
        self.assertEqual(vending_machine.product_inventory["fizzy"], 4)

    def test_buy_still_exact_when_order_points_to_still(self):
        vending_machine.current_order_index = 1  # selling_order[1] == "still"
        vending_machine.insert_coin(10)
        vending_machine.insert_coin(10)
        vending_machine.insert_coin(10)  # total 30
        message = vending_machine.purchase_water("still")
        self.assertIn("Dispensed: Still Water", message)
        self.assertIn("Change $0", message)
        self.assertEqual(vending_machine.product_inventory["still"], 4)

    def test_change_is_given_when_possible(self):
        vending_machine.current_order_index = 0  # required = fizzy
        vending_machine.insert_coin(10)
        vending_machine.insert_coin(10)
        vending_machine.insert_coin(10)
        vending_machine.insert_coin(10)  # total 40
        message = vending_machine.purchase_water("fizzy")  # price 35 -> $5 change
        self.assertIn("Dispensed: Fizzy Water", message)
        self.assertIn("Change $5", message)

    def test_sale_completes_with_zero_change_if_exact_change_not_possible(self):
        # No coins for change -> $0 change but sale still goes through
        vending_machine.set_inventory({"still": 5, "fizzy": 5}, {1: 0, 2: 0, 5: 0, 10: 0})
        vending_machine.current_order_index = 0
        vending_machine.insert_coin(10)
        vending_machine.insert_coin(10)
        vending_machine.insert_coin(10)
        vending_machine.insert_coin(10)  # total 40
        message = vending_machine.purchase_water("fizzy")  # needs $5 change; not possible
        self.assertIn("Dispensed: Fizzy Water", message)
        self.assertIn("Change $0", message)
        self.assertEqual(vending_machine.product_inventory["fizzy"], 4)

    def test_order_enforces_required_product(self):
        vending_machine.current_order_index = 0  # required = fizzy
        vending_machine.insert_coin(10)
        vending_machine.insert_coin(10)
        vending_machine.insert_coin(10)  # total 30
        message = vending_machine.purchase_water("still")
        self.assertIn("Please choose:", message)
        # No inventory change when refused
        self.assertEqual(vending_machine.product_inventory["still"], 5)
        self.assertEqual(vending_machine.product_inventory["fizzy"], 5)

    def test_insufficient_funds(self):
        vending_machine.current_order_index = 1  # required = still
        vending_machine.insert_coin(10)
        vending_machine.insert_coin(10)  # total 20
        message = vending_machine.purchase_water("still")  # price 30
        self.assertIn("Insufficient funds", message)
        self.assertEqual(vending_machine.product_inventory["still"], 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
