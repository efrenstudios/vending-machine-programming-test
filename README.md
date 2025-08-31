# Vending Machine Programming Test
Hiring test, minimal vending machine in plain Python

# Problem
## Vending Machine
 
Write a vending machine in Python with these features:

- It should sell still and fizzy water in 2 to 3 proportions
- The still should cost 30, the fizzy 35 money
- For buying a bottle It should accept 1, 2, 5 and 10 money coins
- It should give change
- It should track inventory
- We will run it in Python version 3.7 to 3.9.

 Please write a testing module.
 
 Please store solutions online in a repository.

# My approach 

- I am **not a Python expert**. I have used older versions  in the past, and I wanted something that also runs on Python 2 while staying compatible with Python 3.7–3.9 as required.
- I chose to **use no libraries**. This lets the reviewers see my **plain Python** and my problem-solving style without extra tools.
- I like **clear functions and simple data**, and I usually lean toward **C++/OOP** ideas. For this small exercise, I intentionally kept things **very minimal and traditional** to match the scope.
- I took **practical liberties**: I only implemented exactly what was asked. This is **not** production code; it is a **first pass** that solves the given problem. Validation is **minimal on purpose**.
- I kept variable names descriptive and comments short and necessary. The code is a small, readable MVP that can be extended later if needed.
- I assume this exercise runs **“in the void”** (no UI, no persistence, no scaling, no devops). I am not aiming for a future project here, only to meet the exact request with a clear starting point.

# What the program does

- **Products and prices:** Still = 30, Fizzy = 35.
- **Accepts coins:** 1, 2, 5, 10.
- **Inventory tracking:** inventory is stored per product and is reduced when a bottle is dispensed.
- **Provides Change:**
  - Inserted money is first added to the machine’s coin inventory.
  - The machine tries to build exact change using coins 10, 5, 2, then 1 (simple, step by step).
  - If exact change is possible, it gives that amount.
  - If exact change is not possible, the sale still completes and the change is $0. This keeps the MVP very simple.
- 2 to 3 proportion approach:
  - I use a fixed repeating order to keep the 2:3 idea practical: *["fizzy", "still", "fizzy", "still", "fizzy"].*
  - If the required product in that order has inventory, the machine asks for that one.
  - If the required product is out of inventory, it allows the other product.

# Design details
- **Versions:** Written to run cleanly on Python 3.7–3.9. I avoided features that would block Python 2 style reading (no type hints, no f-strings, no pattern matching).
- **No libraries:** Only the Python standard language features are used.
- Small set of module-level variables for prices, product inventory, coin inventory, inserted balance, and the current position in the selling order.
- **Proportion rule (2:3):** A short list holds the order and an index moves forward after each sale. When the required item has zero inventory, the search skips to the next available item.
- **Change logic:** Inserted total is converted into 10/5/2/1 and added to the machine; then change is built from those same denominations, largest to smallest. No fancy math or search just straight steps.
- **Messages:** Short and clear. **Example:** `Dispensed: Still Water. Change $15.`

# API 
File: **vending_machine.py**

- **set_inventory(new_product_inventory, new_coin_inventory)** Set starting inventory and coin inventory (non-negative integers, products are only "still" and "fizzy", coins are only 1,2,5,10). Resets the inserted balance to zero.
- **insert_coin(coin)** Accept 1, 2, 5, or 10. Returns a short message with the updated balance.
- purchase_water(requested_product) requested_product is "still" or "fizzy". Applies the 2:3 order rule, checks funds, tries to give change, updates inventory, advances the order, and clears the inserted balance. Returns a short message like: `Dispensed: Still Water. Change $15`
- 

# Testing module
File: **test_vending_machine.py**

This uses Python’s built-in unittest. It checks: exact purchases, change given when possible, sale with change $0 when not possible, order enforcement, inventory decrement, and basic validation.

# Design notes 

- **State:** kept as module-level variables. This is fine for a small exercise. Globals are used where needed (for reassignment); dict updates do not require global.
- **Giving change:** I break the available money into 10, 5, 2, 1, in that order, to try to form the exact change. If exact change is possible, I subtract those coins from the coin inventory and report the change amount. If it is not possible, I complete the sale with Change $0.
- **2 to 3 proportion:** I use a simple list and a pointer that moves forward each time. If the required product has inventory, I ask for that one. If it does not, I allow the other product. Didn't designed anything complicated neither check edge cases, neither give the user flexibility on this.
- **Messages:** short and readable like `Dispensed: Fizzy Water. Change $5`
- **coin_inventory:** Gave the machine a random number of coins at the begining, no big decision behind this.

# Assumptions and limits (on purpose)

- **Minimal validation only.** Inputs are expected to be "still" or "fizzy" and coin values in {1,2,5,10}.
- **Not concurrent.** This is a small, single-user, small MVP.  
- **Not modularized.** No packages, no layers, no I/O. Just the essentials to meet the spec.
- **Change behavior** I kept it strict on purpose—give exact change only if the coins exist; otherwise complete the sale with $0 change—to keep the App small, avoid extra verification/branches, and make the logic easy to read and test within the assignment scope.
