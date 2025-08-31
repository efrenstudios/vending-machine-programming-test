# vending_machine.py

# prices and product inventory
prices_by_product = {"still": 30, "fizzy": 35}
product_inventory = {"still": 5, "fizzy": 5}

# coin inventory used to give change (random initial values)
coin_inventory = {1: 50, 2: 20, 5: 10, 10: 10}

# money inserted for the current purchase (single total)
inserted_total = 0

# 2 to 3 selling order (repeat forever)
selling_order = ["fizzy", "still", "fizzy", "still", "fizzy"]
current_order_index = 0


def set_inventory(new_product_inventory, new_coin_inventory):
    # set initial product inventory and coin inventory with basic validation.
    global inserted_total

    # products... only 'still' and 'fizzy', non-negative integers
    if new_product_inventory is not None:
        if "still" in new_product_inventory:
            units = new_product_inventory["still"]
            if type(units) is int and units >= 0:
                product_inventory["still"] = units
            else:
                return "Invalid inventory for still."
        if "fizzy" in new_product_inventory:
            units = new_product_inventory["fizzy"]
            if type(units) is int and units >= 0:
                product_inventory["fizzy"] = units
            else:
                return "Invalid inventory for fizzy."

    # coins... only 1,2,5,10, non-negative integers
    if new_coin_inventory is not None:
        for coin in (1, 2, 5, 10):
            if coin in new_coin_inventory:
                count = new_coin_inventory[coin]
                if type(count) is int and count >= 0:
                    coin_inventory[coin] = count
                else:
                    return "Invalid coin inventory."

    inserted_total = 0
    return "Inventory set."


def insert_coin(coin):
    # Accept 1, 2, 5 or 10. Return a short message with the new balance.
    global inserted_total
    if coin not in (1, 2, 5, 10):
        return "Invalid coin."
    inserted_total += coin
    return "Accepted {0}. Balance ${1}".format(coin, inserted_total)


def purchase_water(requested_product):
    
    # sell 'still' or 'fizzy'.
    # - keep 2 to 3 order, if the required one has inventory, ask for it.
    # - give change if possible, otherwise complete the sale with Change $0.
    # - decrease product inventory by 1 on success.
    # - inserted money is added to coin inventory before attempting change.
    
    global inserted_total, current_order_index

    # product name must be exactly 'still' or 'fizzy'
    if requested_product not in prices_by_product:
        return "Unknown product."

    # find the product that should be sold now (respect order, skip empty)
    required_product = None
    order_length = len(selling_order)
    for offset_in_order in range(order_length):
        position = (current_order_index + offset_in_order) % order_length
        candidate_product = selling_order[position]
        if product_inventory.get(candidate_product, 0) > 0:
            required_product = candidate_product
            current_order_index = position
            break
    if required_product is None:
        return "Out of stock."

    # if a different product was requested and the required has inventory, ask for the required one
    if requested_product != required_product and product_inventory.get(required_product, 0) > 0:
        if required_product == "still":
            label = "Still Water"
        else:
            label = "Fizzy Water"
        return "Please choose: {0}".format(label)

    # check inventory of requested item
    if product_inventory.get(requested_product, 0) <= 0:
        return "No inventory for {0}.".format(requested_product)

    # check funds
    price = prices_by_product[requested_product]
    if inserted_total < price:
        return "Insufficient funds. Price ${0}, balance ${1}".format(price, inserted_total)

    # add inserted_total into coin_inventory, then attempt change using that pool
    # break inserted_total into 10, 5, 2, 1 and add to coin inventory
    remaining_to_add = inserted_total
    
    # using // instead of / for floor division.  I know the test should be considered mostly for python 3.7 onwards but wanted to keep it simple and compatible with python 2

    add_10 = remaining_to_add // 10
    remaining_to_add = remaining_to_add - add_10 * 10

    add_5 = remaining_to_add // 5
    remaining_to_add = remaining_to_add - add_5 * 5

    add_2 = remaining_to_add // 2
    remaining_to_add = remaining_to_add - add_2 * 2

    add_1 = remaining_to_add // 1
    remaining_to_add = remaining_to_add - add_1 * 1

    if add_10 > 0:
        coin_inventory[10] = coin_inventory.get(10, 0) + add_10
    if add_5 > 0:
        coin_inventory[5] = coin_inventory.get(5, 0) + add_5
    if add_2 > 0:
        coin_inventory[2] = coin_inventory.get(2, 0) + add_2
    if add_1 > 0:
        coin_inventory[1] = coin_inventory.get(1, 0) + add_1

    # try to assemble exact change.  If not possible, change will be $0
    change_needed = inserted_total - price
    change_given = 0

    if change_needed > 0:
        remaining_change = change_needed

        use_10 = min(remaining_change // 10, coin_inventory.get(10, 0))
        remaining_change = remaining_change - use_10 * 10

        use_5 = min(remaining_change // 5, coin_inventory.get(5, 0))
        remaining_change = remaining_change - use_5 * 5

        use_2 = min(remaining_change // 2, coin_inventory.get(2, 0))
        remaining_change = remaining_change - use_2 * 2

        use_1 = min(remaining_change // 1, coin_inventory.get(1, 0))
        remaining_change = remaining_change - use_1 * 1

        if remaining_change == 0:
            coin_inventory[10] = coin_inventory.get(10, 0) - use_10
            coin_inventory[5] = coin_inventory.get(5, 0) - use_5
            coin_inventory[2] = coin_inventory.get(2, 0) - use_2
            coin_inventory[1] = coin_inventory.get(1, 0) - use_1
            change_given = change_needed
        else:
            change_given = 0  # sale still completes with $0 change

    # complete the sale
    product_inventory[requested_product] = product_inventory.get(requested_product, 0) - 1
    current_order_index = (current_order_index + 1) % len(selling_order)

    if requested_product == "still":
        dispensed_label = "Still Water"
    else:
        dispensed_label = "Fizzy Water"

    inserted_total = 0

    return "Dispensed: {0}. Change ${1}".format(dispensed_label, change_given)
