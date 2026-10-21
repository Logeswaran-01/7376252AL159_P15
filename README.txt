Name: Logeswaran B
Register Number: 7376252AL159
Project: P15 - StockSmart Shop Inventory Manager

Description
A simple Python program to manage the stock of a stationery shop. It records
purchases and sales, prints a bill for every sale, warns when an item is
running low, and shows the stock value and the profit earned.

Features
* Add product (code, name, category, cost price, selling price, stock, reorder level)
* Record purchase (stock in)
* Record sale (stock out) with a bill showing quantity, price, total and stock left
* View / search products
* Low-stock alert (stock at or below the reorder level)
* Stock value at cost price, per category and in total
* Profit report (calculated from the prices saved with each sale)
* Edit product
* Delete product (with confirmation)

Input Checks
* Duplicate product codes are rejected
* Prices must be numbers greater than 0
* Stock and reorder level must be whole numbers, 0 or more
* A sale larger than the available stock is refused
* Invalid dates, wrong menu choices, letters, empty input and the | character are rejected
* The program never crashes on wrong input and works on the first run without data files

Data Files
* products.txt – Code|Name|Category|CostPrice|SellingPrice|Stock|ReorderLevel
* sales.txt – Date|Code|Quantity|SellingPrice|CostPrice
* sample_run.txt – copy of the terminal session of the latest run (replaced on every run)

Requirements
* Python 3.x (no imports, no external libraries)

How to Run
1. Keep main.py, products.txt and sales.txt in the same folder.
2. Open a terminal in the project folder.
3. Run:
   python main.py

Menu Options
1. Add product
2. Record purchase
3. Record sale
4. View / search products
5. Low-stock alert
6. Stock value
7. Profit report
8. Edit product
9. Delete product
0. Exit

Bonus Features Done
None

Known Problems
None known

Language
Python
