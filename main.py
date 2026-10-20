# constant decalartion
PRODUCTS_FILE = "products.txt"
SALES_FILE = "sales.txt"
LOG_FILE = "sample_run.txt"  
# output/input 
def show(text=""):
    print(text)
    file = open(LOG_FILE, "a")
    file.write(str(text) + "\n")
    file.close()
def ask(prompt):
    # asking the input
    answer = input(prompt)
    file = open(LOG_FILE, "a")
    file.write(prompt + answer + "\n")
    file.close()
    return answer
# input file handler
def get_text(prompt):
    #asking the user until they dont enter | or empty string
    while True:
        text = ask(prompt).strip()
        if text == "":
            show("Input cannot be empty.")
        elif "|" in text:
            show("The | character is not allowed.")
        else:
            return text
        
def get_int(prompt, low, high):
    # asking user until they type the whole number between low and high price
    while True:
        text = ask(prompt).strip()
        try:
            number = int(text)
        except ValueError:
            show("Please enter a whole number.")
            continue
        if number < low or number > high:
            show(f"Number must be between {low} and {high}.")
        else:
            return number
        
def get_price(prompt):
    # keep asking until the user types a number greater than 0
    while True:
        text = ask(prompt).strip()
        try:
            number = float(text)
        except ValueError:
            show("Please enter a number like 45 or 45.50.")
            continue
        if number > 0 and number < 10000000:
            return number
        show("Price must be greater than 0 and lesser than 10000000.")

# data correctness
def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def get_date():
    # keep asking until the user types a real date like 16-10-2026
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    while True:
        text = ask("Enter today's date (DD-MM-YYYY): ").strip() #it removes extra space
        parts = text.split("-")
        if len(parts) == 3 and parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
            day = int(parts[0])
            month = int(parts[1])
            year = int(parts[2])
            if month >= 1 and month <= 12 and year >= 2000:
                last_day = days_in_month[month - 1]
                if month == 2 and is_leap_year(year):
                    last_day = 29
                if day >= 1 and day <= last_day:
                    return text
        show("Invalid date. Example: 16-10-2026")


# sample data functions
def load_products():
    # read products.txt into a list of dictionaries
    products = []
    try:
        file = open(PRODUCTS_FILE, "r")
        for line in file:
            parts = line.strip().split("|")
            if len(parts) == 7 and parts[0] != "Code":
                try:
                    product = {
                        "code": parts[0],
                        "name": parts[1],
                        "category": parts[2],
                        "cost": float(parts[3]),
                        "sell": float(parts[4]),
                        "stock": int(parts[5]),
                        "reorder": int(parts[6]),
                    }
                    products.append(product)
                except ValueError:
                    pass #it skip the damaged line
        file.close()
    except FileNotFoundError:
        pass  # no file exists
    return products


def save_products(products):
    # write every product back to products.txt
    file = open(PRODUCTS_FILE, "w")
    file.write("Code|Name|Category|CostPrice|SellingPrice|Stock|ReorderLevel\n")
    for p in products:
        file.write(f"{p['code']}|{p['name']}|{p['category']}|{p['cost']:.2f}|"
                   f"{p['sell']:.2f}|{p['stock']}|{p['reorder']}\n")
    file.close()


def save_sale(date, code, qty, sell, cost):
    # add one line at the end of sales.txt
    try:
        open(SALES_FILE, "r").close()
        is_new = False
    except FileNotFoundError:
        is_new = True
    file = open(SALES_FILE, "a")
    if is_new:
        file.write("Date|Code|Quantity|SellingPrice|CostPrice\n")
    file.write(f"{date}|{code}|{qty}|{sell:.2f}|{cost:.2f}\n")
    file.close()


def find_product(products, code):
    # return the product with this code, or None if not found
    for p in products:
        if p["code"] == code:
            return p
    return None


# menu features
def add_product(products):
    code = get_text("Product code: ").upper()
    if find_product(products, code) is not None:
        show("This code already exists.")
        return
    name = get_text("Name: ")
    category = get_text("Category: ")
    cost = get_price("Cost price: ")
    sell = get_price("Selling price: ")
    if sell < cost:
        show("Warning: selling price is below cost price!")
    stock = get_int("Stock quantity: ", 0, 1000000)
    reorder = get_int("Reorder level: ", 0, 1000000)
    products.append({"code": code, "name": name, "category": category,
                     "cost": cost, "sell": sell, "stock": stock, "reorder": reorder})
    save_products(products)
    show("Product added.")


def record_purchase(products):
    code = ask("Product code: ").strip().upper()
    product = find_product(products, code)
    if product is None:
        show("Product not found.")
        return
    qty = get_int("Quantity purchased: ", 1, 1000000)
    product["stock"] = product["stock"] + qty
    save_products(products)
    show(f"Done. New stock of {product['name']}: {product['stock']}")


def record_sale(products):
    code = ask("Product code: ").strip().upper()
    product = find_product(products, code)
    if product is None:
        show("Product not found.")
        return
    show(f"{product['name']} - in stock: {product['stock']}")
    if product["stock"] == 0:
        show("Out of stock.")
        return
    qty = get_int("Quantity sold: ", 1, 1000000)
    if qty > product["stock"]:
        show(f"Not enough stock. Only {product['stock']} available.")
        return
    date = get_date()
    product["stock"] = product["stock"] - qty        # reduce stock
    save_sale(date, product["code"], qty, product["sell"], product["cost"])
    save_products(products)
    # print the bill
    total = qty * product["sell"]
    show("\n------ BILL ------")
    show(f"Product: {product['name']}")
    show(f"{qty} x Rs. {product['sell']:.2f} = Rs. {total:.2f}")
    show(f"Stock left: {product['stock']}")
    show("------------------")
    if product["stock"] <= product["reorder"]:
        show("Warning: this item is now low on stock!")


def view_products(products):
    keyword = ask("Search by name or code (Enter = show all): ").strip().lower()
    count = 0
    for p in products:
        if keyword in p["name"].lower() or keyword in p["code"].lower():
            show(f"{p['code']} | {p['name']} | {p['category']} | cost {p['cost']:.2f} | "
                  f"sell {p['sell']:.2f} | stock {p['stock']} | reorder {p['reorder']}")
            count = count + 1
    if count == 0:
        show("No products found.")


def low_stock(products):
    count = 0
    for p in products:
        if p["stock"] <= p["reorder"]:       # at or below, so <=
            show(f"{p['code']} {p['name']} stock {p['stock']} (reorder at {p['reorder']})")
            count = count + 1
    if count == 0:
        show("No product is running low.")


def stock_value(products):
    totals = {}                               # category -> total value
    grand_total = 0
    for p in products:
        value = p["cost"] * p["stock"]
        if p["category"] in totals:
            totals[p["category"]] = totals[p["category"]] + value
        else:
            totals[p["category"]] = value
        grand_total = grand_total + value
    for category in totals:
        show(f"{category}: Rs. {totals[category]:.2f}")
    show(f"GRAND TOTAL: Rs. {grand_total:.2f}")


def profit_report(products):
    total_profit = 0
    try:
        file = open(SALES_FILE, "r")
        for line in file:
            parts = line.strip().split("|")
            if len(parts) == 5 and parts[0] != "Date":
                try:
                    qty = int(parts[2])
                    sell = float(parts[3])
                    cost = float(parts[4])
                    total_profit = total_profit + (sell - cost) * qty
                except ValueError:
                    pass
        file.close()
    except FileNotFoundError:
        pass
    show(f"Total profit: Rs. {total_profit:.2f}")


def edit_product(products):
    code = ask("Product code to edit: ").strip().upper()
    product = find_product(products, code)
    if product is None:
        show("Product not found.")
        return
    show("1. Name  2. Category  3. Cost price  4. Selling price  5. Stock  6. Reorder level")
    choice = get_int("What to change: ", 1, 6)
    if choice == 1:
        product["name"] = get_text("New name: ")
    elif choice == 2:
        product["category"] = get_text("New category: ")
    elif choice == 3:
        product["cost"] = get_price("New cost price: ")
    elif choice == 4:
        product["sell"] = get_price("New selling price: ")
    elif choice == 5:
        product["stock"] = get_int("New stock: ", 0, 1000000)
    else:
        product["reorder"] = get_int("New reorder level: ", 0, 1000000)
    save_products(products)
    show("Product updated.")


def delete_product(products):
    code = ask("Product code to delete: ").strip().upper()
    product = find_product(products, code)
    if product is None:
        show("Product not found.")
        return
    answer = ask(f"Delete {product['name']}? (y/n): ").strip().lower()
    if answer == "y":
        products.remove(product)
        save_products(products)
        show("Product deleted.")
    else:
        show("Cancelled.")


# ---------- Menu ----------
def show_menu():
    show("\n===== STOCKSMART MENU =====")
    show("1. Add product          2. Record purchase")
    show("3. Record sale          4. View / search products")
    show("5. Low-stock alert      6. Stock value")
    show("7. Profit report        8. Edit product")
    show("9. Delete product       0. Exit")


def main():
    open(LOG_FILE, "w").close()      # new run: erase the old content of sample_run.txt
    products = load_products()
    while True:
        show_menu()
        choice = get_int("Enter choice: ", 0, 9)
        if choice == 1:
            add_product(products)
        elif choice == 2:
            record_purchase(products)
        elif choice == 3:
            record_sale(products)
        elif choice == 4:
            view_products(products)
        elif choice == 5:
            low_stock(products)
        elif choice == 6:
            stock_value(products)
        elif choice == 7:
            profit_report(products)
        elif choice == 8:
            edit_product(products)
        elif choice == 9:
            delete_product(products)
        else:
            show("Goodbye!")
            break


main()
