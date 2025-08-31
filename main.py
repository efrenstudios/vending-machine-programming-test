
# Commented simple test bellow
# import vending_machine as vm

# vm.set_inventory({"still": 2, "fizzy": 2}, {1: 5, 2: 5, 5: 5, 10: 5})
# print(vm.insert_coin(10))
# print(vm.insert_coin(10))
# print(vm.insert_coin(10))
# print(vm.purchase_water("still"))



# main.py  
# Is the actual implemented main in cases that needed.
#discovers and runs tests

import unittest

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover(".", pattern="test_*.py")
    unittest.TextTestRunner(verbosity=2).run(suite)
