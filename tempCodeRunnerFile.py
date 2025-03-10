import tkinter as tk
from tkinter import messagebox
import csv
import os

class ZoozooApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zoozoo - HomelyShopping")
        self.root.config(bg="#f0f8ff")
        self.create_home_page()

    def create_home_page(self):
        # Homepage layout with clickable buttons (images can be added later)
        button_frame = tk.Frame(self.root, bg="#f0f8ff")
        button_frame.pack(pady=20)

        # Meal Planner Button
        meal_planner_btn = tk.Button(button_frame, text="Meal Planner", command=self.open_meal_planner, height=3, width=20, bg="#ADD8E6", font=("Helvetica", 12, "bold"))
        meal_planner_btn.grid(row=0, column=0, padx=10, pady=10)

        # Recipe Planner Button
        recipe_planner_btn = tk.Button(button_frame, text="Recipe Planner", command=self.open_recipe_planner, height=3, width=20, bg="#FFA07A", font=("Helvetica", 12, "bold"))
        recipe_planner_btn.grid(row=0, column=1, padx=10, pady=10)

        # Grocery Store Button
        grocery_store_btn = tk.Button(button_frame, text="Grocery Store", command=self.open_grocery_store, height=3, width=20, bg="#98FB98", font=("Helvetica", 12, "bold"))
        grocery_store_btn.grid(row=1, column=0, padx=10, pady=10)

        # Cart Button
        cart_btn = tk.Button(button_frame, text="Cart", command=self.open_cart, height=3, width=20, bg="#FFD700", font=("Helvetica", 12, "bold"))
        cart_btn.grid(row=1, column=1, padx=10, pady=10)

    # Open Meal Planner
    def open_meal_planner(self):
        MealPlanner(self.root)

    # Open Recipe Planner
    def open_recipe_planner(self):
        RecipePlanner(self.root)

    # Open Grocery Store
    def open_grocery_store(self):
        GroceryStore(self.root)

    # Open Cart
    def open_cart(self):
        CartPage(self.root)

class MealPlanner:
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Meal Planner")
        self.top.config(bg="#f0f8ff")
        self.create_meal_form()

    def create_meal_form(self):
        tk.Label(self.top, text="Meal Planner", font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(pady=10)

        # Form for inputting meal details
        self.meal_type_var = tk.StringVar(value="Breakfast")
        self.date_var = tk.StringVar()
        self.time_var = tk.StringVar()

        tk.Label(self.top, text="Date (YYYY-MM-DD):", bg="#f0f8ff").pack()
        tk.Entry(self.top, textvariable=self.date_var).pack(pady=5)

        tk.Label(self.top, text="Time (HH:MM):", bg="#f0f8ff").pack()
        tk.Entry(self.top, textvariable=self.time_var).pack(pady=5)

        tk.Label(self.top, text="Meal Type:", bg="#f0f8ff").pack()
        tk.OptionMenu(self.top, self.meal_type_var, "Breakfast", "Lunch", "Dinner").pack(pady=5)

        tk.Button(self.top, text="Save Meal", command=self.save_meal, bg="#90EE90").pack(pady=10)

        self.display_meals()

    def save_meal(self):
        meal_data = [self.meal_type_var.get(), self.date_var.get(), self.time_var.get()]
        with open('meals.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(meal_data)
        messagebox.showinfo("Success", "Meal saved successfully!")
        self.display_meals()

    def display_meals(self):
        tk.Label(self.top, text="Your Meals:", font=("Helvetica", 14, "bold"), bg="#f0f8ff").pack(pady=10)
        try:
            with open('meals.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:
                        tk.Label(self.top, text=f"{row[0]} on {row[1]} ({row[2]})", bg="#f0f8ff").pack()
                    else:
                        print("Warning: Row does not have enough data:", row)
        except FileNotFoundError:
            tk.Label(self.top, text="No meals saved yet.", bg="#f0f8ff").pack()

class RecipePlanner:
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Recipe Planner")
        self.top.config(bg="#f0f8ff")
        self.create_recipe_form()

    def create_recipe_form(self):
        tk.Label(self.top, text="Recipe Planner", font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(pady=10)

        # Form for inputting recipe details
        self.recipe_name_var = tk.StringVar()
        self.recipe_desc_var = tk.StringVar()

        tk.Label(self.top, text="Recipe Name:", bg="#f0f8ff").pack()
        tk.Entry(self.top, textvariable=self.recipe_name_var).pack(pady=5)

        tk.Label(self.top, text="Description:", bg="#f0f8ff").pack()
        tk.Entry(self.top, textvariable=self.recipe_desc_var).pack(pady=5)

        tk.Button(self.top, text="Save Recipe", command=self.save_recipe, bg="#90EE90").pack(pady=10)

        self.display_recipes()

    def save_recipe(self):
        recipe_data = [self.recipe_name_var.get(), self.recipe_desc_var.get()]
        with open('recipes.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(recipe_data)
        messagebox.showinfo("Success", "Recipe saved successfully!")
        self.display_recipes()

    def display_recipes(self):
        tk.Label(self.top, text="Your Recipes:", font=("Helvetica", 14, "bold"), bg="#f0f8ff").pack(pady=10)
        try:
            with open('recipes.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 2:
                        tk.Label(self.top, text=f"{row[0]}: {row[1]}", bg="#f0f8ff").pack()
                    else:
                        print("Warning: Row does not have enough data:", row)
        except FileNotFoundError:
            tk.Label(self.top, text="No recipes saved yet.", bg="#f0f8ff").pack()

class GroceryStore:
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Grocery Store")
        self.top.config(bg="#f0f8ff")
        self.create_grocery_store()

    def create_grocery_store(self):
        groceries = self.load_groceries_from_csv()

        # Create a canvas and scrollbar for the store
        self.canvas = tk.Canvas(self.top, bg="#f0f8ff")
        self.scrollbar = tk.Scrollbar(self.top, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas
        self.store_frame = tk.Frame(self.canvas, bg="#f0f8ff")
        self.store_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.store_frame, anchor="nw")

        # Pack the canvas and scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(self.store_frame, text="Available Groceries:", font=("Helvetica", 14, "bold"), bg="#f0f8ff").grid(row=0, column=0, columnspan=4, pady=10)

        # Display grocery items in a grid (4 items per row)
        row = 1
        col = 0
        for name, price in groceries:
            grocery_item = GroceryItem(name, price)
            self.add_grocery_item(grocery_item, row, col)
            col += 1
            if col > 3:  # Wrap to the next line after 4 items
                col = 0
                row += 1

    def load_groceries_from_csv(self):
        groceries = []
        try:
            with open('groceries.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 2:
                        groceries.append((row[0], row[1]))  # Name and Price
        except FileNotFoundError:
            groceries = [("Apple", "100"), ("Banana", "40"), ("Milk", "50"), ("Bread", "30")]  # Default items
        return groceries

    def add_grocery_item(self, grocery_item, row, col):
        item_frame = tk.Frame(self.store_frame, bg="#f0f8ff", padx=10, pady=10, relief=tk.GROOVE, bd=2)
        item_frame.grid(row=row, column=col, padx=10, pady=10)

        tk.Label(item_frame, text=grocery_item.display_item(), font=("Helvetica", 12), bg="#f0f8ff").pack(pady=5)
        add_to_cart_btn = tk.Button(item_frame, text="Add to Cart", command=lambda item=grocery_item.name: self.add_to_cart(item), bg="#90EE90")
        add_to_cart_btn.pack()

    def add_to_cart(self, item):
        with open('cart.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([item])
        messagebox.showinfo("Success", f"{item} has been added to your cart!")

class GroceryItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def display_item(self):
        return f"{self.name}\nPrice: {self.price} INR"

class CartPage:
    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Cart")
        self.top.config(bg="#f0f8ff")
        self.display_cart_items()

    def display_cart_items(self):
        tk.Label(self.top, text="Your Cart:", font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(pady=10)
        try:
            with open('cart.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        tk.Label(self.top, text=f"{row[0]}", bg="#f0f8ff").pack()
        except FileNotFoundError:
            tk.Label(self.top, text="Your cart is empty.", bg="#f0f8ff").pack()

        tk.Button(self.top, text="Checkout", command=self.checkout, bg="#FFD700").pack(pady=20)

    def checkout(self):
        if os.path.exists('cart.csv'):
            os.remove('cart.csv')  # Clear the cart after checkout
        messagebox.showinfo("Success", "Your order has been placed!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZoozooApp(root)
    root.mainloop()
import tkinter as tk
from tkinter import messagebox
import csv
import os

# Base class for common functionalities
class BasePage:
    def __init__(self, root):
        self.root = root
        self.root.config(bg="#f0f8ff")
    
    def show_message(self, title, message):
        messagebox.showinfo(title, message)

    def load_csv(self, filename):
        try:
            with open(filename, mode='r') as file:
                reader = csv.reader(file)
                return [row for row in reader]
        except FileNotFoundError:
            return []

    def save_to_csv(self, filename, data):
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def clear_csv(self, filename):
        if os.path.exists(filename):
            os.remove(filename)

class ZoozooApp(BasePage):
    def __init__(self, root):
        super().__init__(root)
        self.root.title("Zoozoo - HomelyShopping")
        self.create_home_page()

    def create_home_page(self):
        button_frame = tk.Frame(self.root, bg="#f0f8ff")
        button_frame.pack(pady=20)

        buttons = [
            ("Meal Planner", self.open_meal_planner, "#ADD8E6"),
            ("Recipe Planner", self.open_recipe_planner, "#FFA07A"),
            ("Grocery Store", self.open_grocery_store, "#98FB98"),
            ("Cart", self.open_cart, "#FFD700")
        ]

        for index, (text, command, color) in enumerate(buttons):
            tk.Button(button_frame, text=text, command=command, height=3, width=20, bg=color,
                      font=("Helvetica", 12, "bold")).grid(row=index // 2, column=index % 2, padx=10, pady=10)

    def open_meal_planner(self):
        MealPlanner(self.root)

    def open_recipe_planner(self):
        RecipePlanner(self.root)

    def open_grocery_store(self):
        GroceryStore(self.root)

    def open_cart(self):
        CartPage(self.root)


class MealPlanner(BasePage):
    def __init__(self, root):
        super().__init__(tk.Toplevel(root))
        self.top.title("Meal Planner")
        self.create_meal_form()

    def create_meal_form(self):
        tk.Label(self.top, text="Meal Planner", font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(pady=10)

        self.meal_type_var = tk.StringVar(value="Breakfast")
        self.date_var = tk.StringVar()
        self.time_var = tk.StringVar()

        self.create_form_entry("Date (YYYY-MM-DD):", self.date_var)
        self.create_form_entry("Time (HH:MM):", self.time_var)

        tk.Label(self.top, text="Meal Type:", bg="#f0f8ff").pack()
        tk.OptionMenu(self.top, self.meal_type_var, "Breakfast", "Lunch", "Dinner").pack(pady=5)

        tk.Button(self.top, text="Save Meal", command=self.save_meal, bg="#90EE90").pack(pady=10)
        self.display_meals()

    def create_form_entry(self, label_text, variable):
        tk.Label(self.top, text=label_text, bg="#f0f8ff").pack()
        tk.Entry(self.top, textvariable=variable).pack(pady=5)

    def save_meal(self):
        meal_data = [self.meal_type_var.get(), self.date_var.get(), self.time_var.get()]
        self.save_to_csv('meals.csv', meal_data)
        self.show_message("Success", "Meal saved successfully!")
        self.display_meals()

    def display_meals(self):
        tk.Label(self.top, text="Your Meals:", font=("Helvetica", 14, "bold"), bg="#f0f8ff").pack(pady=10)
        meals = self.load_csv('meals.csv')
        if meals:
            for meal in meals:
                if len(meal) >= 3:
                    tk.Label(self.top, text=f"{meal[0]} on {meal[1]} ({meal[2]})", bg="#f0f8ff").pack()
        else:
            tk.Label(self.top, text="No meals saved yet.", bg="#f0f8ff").pack()


class RecipePlanner(BasePage):
    def __init__(self, root):
        super().__init__(tk.Toplevel(root))
        self.top.title("Recipe Planner")
        self.create_recipe_form()

    def create_recipe_form(self):
        tk.Label(self.top, text="Recipe Planner", font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(pady=10)

        self.recipe_name_var = tk.StringVar()
        self.recipe_desc_var = tk.StringVar()

        self.create_form_entry("Recipe Name:", self.recipe_name_var)
        self.create_form_entry("Description:", self.recipe_desc_var)

        tk.Button(self.top, text="Save Recipe", command=self.save_recipe, bg="#90EE90").pack(pady=10)
        self.display_recipes()

    def create_form_entry(self, label_text, variable):
        tk.Label(self.top, text=label_text, bg="#f0f8ff").pack()
        tk.Entry(self.top, textvariable=variable).pack(pady=5)

    def save_recipe(self):
        recipe_data = [self.recipe_name_var.get(), self.recipe_desc_var.get()]
        self.save_to_csv('recipes.csv', recipe_data)
        self.show_message("Success", "Recipe saved successfully!")
        self.display_recipes()

    def display_recipes(self):
        tk.Label(self.top, text="Your Recipes:", font=("Helvetica", 14, "bold"), bg="#f0f8ff").pack(pady=10)
        recipes = self.load_csv('recipes.csv')
        if recipes:
            for recipe in recipes:
                if len(recipe) >= 2:
                    tk.Label(self.top, text=f"{recipe[0]}: {recipe[1]}", bg="#f0f8ff").pack()
        else:
            tk.Label(self.top, text="No recipes saved yet.", bg="#f0f8ff").pack()


class GroceryStore(BasePage):
    def __init__(self, root):
        super().__init__(tk.Toplevel(root))
        self.top.title("Grocery Store")
        self.create_grocery_store()

    def create_grocery_store(self):
        groceries = self.load_groceries_from_csv()
        self.create_store_layout(groceries)

    def load_groceries_from_csv(self):
        groceries = self.load_csv('groceries.csv')
        if not groceries:
            groceries = [("Apple", "100"), ("Banana", "40"), ("Milk", "50"), ("Bread", "30")]  # Default items
        return groceries

    def create_store_layout(self, groceries):
        self.canvas = tk.Canvas(self.top, bg="#f0f8ff")
        self.scrollbar = tk.Scrollbar(self.top, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.store_frame = tk.Frame(self.canvas, bg="#f0f8ff")
        self.store_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.store_frame, anchor="nw")

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(self.store_frame, text="Available Groceries:", font=("Helvetica", 14, "bold"), bg="#f0f8ff").grid(row=0, column=0, columnspan=4, pady=10)

        row, col = 1, 0
        for name, price in groceries:
            grocery_item = GroceryItem(name, price)
            self.add_grocery_item(grocery_item, row, col)
            col += 1
            if col > 3:
                col, row = 0, row + 1

    def add_grocery_item(self, grocery_item, row, col):
        item_frame = tk.Frame(self.store_frame, bg="#f0f8ff", padx=10, pady=10, relief=tk.GROOVE, bd=2)
        item_frame.grid(row=row, column=col, padx=10, pady=10)

        tk.Label(item_frame, text=grocery_item.display_item(), font=("Helvetica", 12), bg="#f0f8ff").pack(pady=5)
        tk.Button(item_frame, text="Add to Cart", command=lambda: self.add_to_cart(grocery_item.name), bg="#90EE90").pack()

    def add_to_cart(self, item_name):
        self.save_to_csv('cart.csv', [item_name])
        self.show_message("Success", f"{item_name} has been added to your cart!")


class GroceryItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def display_item(self):
        return f"{self.name}\nPrice: {self.price} INR"


class CartPage(BasePage):
    def __init__(self, root):
        super().__init__(tk.Toplevel(root))
        self.top.title("Cart")
        self.display_cart_items()

    def display_cart_items(self):
        tk.Label(self.top, text="Your Cart:", font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(pady=10)
        cart_items = self.load_csv('cart.csv')
        if cart_items:
            for item in cart_items:
                if item:
                    tk.Label(self.top, text=f"{item[0]}", bg="#f0f8ff").pack()
        else:
            tk.Label(self.top, text="Your cart is empty.", bg="#f0f8ff").pack()

        tk.Button(self.top, text="Checkout", command=self.checkout, bg="#FFD700").pack(pady=20)

    def checkout(self):
        self.clear_csv('cart.csv')
        self.show_message("Success", "Your order has been placed!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ZoozooApp(root)
    root.mainloop()
