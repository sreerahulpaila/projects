import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import csv
import os

# ----------------- Database Setup -----------------

def get_db_connection():
    """Connect to the SQLite database."""
    conn = sqlite3.connect('meal_planner.db')
    return conn

def setup_db():
    """Create necessary tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_time TEXT NOT NULL,
            date TEXT NOT NULL,
            meal_type TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groceries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grocery_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (grocery_id) REFERENCES groceries(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS discounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            discount_percent REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def populate_groceries():
    """Populate the groceries table with 100 items if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM groceries")
    count = cursor.fetchone()[0]
    if count >= 100:
        cursor.close()
        conn.close()
        return  # Already populated

    groceries = [
        ('Apples', 100), ('Bananas', 50), ('Oranges', 80), ('Grapes', 120),
        ('Strawberries', 150), ('Blueberries', 200), ('Mangoes', 150),
        ('Pineapples', 120), ('Watermelons', 60), ('Cabbage', 30),
        ('Spinach', 40), ('Carrots', 40), ('Potatoes', 30), ('Onions', 25),
        ('Tomatoes', 50), ('Garlic', 20), ('Ginger', 30), ('Bell Peppers', 60),
        ('Cucumbers', 40), ('Broccoli', 70), ('Cauliflower', 70),
        ('Green Beans', 80), ('Peas', 50), ('Lentils', 100), ('Rice', 70),
        ('Wheat Flour', 40), ('Sugar', 40), ('Salt', 20), ('Black Pepper', 60),
        ('Cumin Seeds', 70), ('Mustard Seeds', 80), ('Soy Sauce', 100),
        ('Olive Oil', 300), ('Coconut Oil', 250), ('Ghee', 400), ('Butter', 250),
        ('Milk', 60), ('Yogurt', 50), ('Cheese', 200), ('Paneer', 200),
        ('Chicken Breast', 300), ('Fish', 250), ('Eggs', 100), ('Rice Flour', 60),
        ('Wheat Flour', 50), ('Oats', 80), ('Chickpeas', 90), ('Peas', 50),
        ('Soy Sauce', 60), ('Tomato Sauce', 50), ('Ketchup', 40), ('Mayonnaise', 80),
        ('Pasta', 70), ('Noodles', 60), ('Corn', 50), ('Beans', 40),
        ('Almonds', 250), ('Cashews', 300), ('Walnuts', 350),
        ('Peanuts', 100), ('Chocolate', 200), ('Biscuits', 50),
        ('Popcorn', 40), ('Tortilla', 60), ('Soda', 30), ('Tea', 150),
        ('Coffee', 300), ('Juice', 90), ('Honey', 150), ('Jam', 80),
        ('Pickles', 70), ('Cereal', 200), ('Granola', 120), ('Muesli', 130),
        ('Coconut Milk', 150), ('Olive Oil', 250), ('Vegetable Oil', 180),
        ('Vinegar', 40), ('Mustard', 60), ('Soy Milk', 100), ('Tofu', 200),
        ('Baking Soda', 30), ('Baking Powder', 30), ('Pudding Mix', 40),
        ('Gelatin', 50), ('Frozen Vegetables', 60), ('Frozen Fruits', 80),
        ('Frozen Pizza', 150), ('Instant Noodles', 30), ('Canned Soup', 60),
        ('Canned Beans', 50), ('Canned Tomatoes', 40), ('Canned Corn', 50),
        ('Banana Chips', 100), ('Trail Mix', 120), ('Energy Bars', 150),
        ('Pancake Mix', 80), ('Maple Syrup', 200), ('Fruit Juice', 90),
        ('Red Wine', 500), ('White Wine', 450), ('Beer', 150), ('Whiskey', 800),
        ('Vodka', 700), ('Rum', 600), ('Gin', 650), ('Tequila', 750),
        ('Lime', 30), ('Lemon', 25), ('Mint Leaves', 20), ('Basil', 20),
        ('Parsley', 20), ('Rosemary', 20), ('Thyme', 20), ('Oregano', 20),
        ('Sage', 20), ('Cilantro', 20), ('Bay Leaves', 20), ('Nutmeg', 50)
    ]

    cursor.executemany("INSERT INTO groceries (name, price) VALUES (?, ?)", groceries)
    conn.commit()
    cursor.close()
    conn.close()

def populate_discounts():
    """Populate the discounts table with sample data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM discounts")
    count = cursor.fetchone()[0]
    if count > 0:
        cursor.close()
        conn.close()
        return  # Already populated

    discounts = [
        ('Vegetables', 50.0),
        ('General Items', 40.0),
        ('Fruits', 30.0),
        ('Dairy Products', 25.0),
        ('Frozen Items', 20.0)
    ]

    cursor.executemany("INSERT INTO discounts (name, discount_percent) VALUES (?, ?)", discounts)
    conn.commit()
    cursor.close()
    conn.close()

# ----------------- Base Planner Class -----------------

class Planner:
    """Base class for MealPlanner and RecipePlanner."""

    def __init__(self, root, title):
        self.top = tk.Toplevel(root)
        self.top.title(title)
        self.top.config(bg="#f0f8ff")
        self.create_form()

    def create_form(self):
        """Method to create form. To be overridden by subclasses."""
        pass

    def submit(self):
        """Method to handle submission. To be overridden by subclasses."""
        pass

    def display_entries(self):
        """Method to display entries. To be overridden by subclasses."""
        pass

# ----------------- MealPlanner Class -----------------

class MealPlanner(Planner):
    """Class for Meal Planner functionality."""

    def __init__(self, root):
        super().__init__(root, "Meal Planner")
        self.display_entries()

    def create_form(self):
        frame = tk.Frame(self.top, bg="#e6f7ff", padx=20, pady=20, bd=2, relief=tk.RAISED)
        frame.pack(pady=20, padx=20)

        tk.Label(frame, text="Meal Time:", bg="#e6f7ff", font=("Helvetica", 12)).grid(row=0, column=0, pady=5, sticky='e')
        self.meal_time_entry = tk.Entry(frame, width=30)
        self.meal_time_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Date (YYYY-MM-DD):", bg="#e6f7ff", font=("Helvetica", 12)).grid(row=1, column=0, pady=5, sticky='e')
        self.date_entry = tk.Entry(frame, width=30)
        self.date_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Type (Breakfast/Lunch/Dinner):", bg="#e6f7ff", font=("Helvetica", 12)).grid(row=2, column=0, pady=5, sticky='e')
        self.type_entry = tk.Entry(frame, width=30)
        self.type_entry.grid(row=2, column=1, pady=5)

        submit_btn = tk.Button(frame, text="Add Meal", command=self.submit, bg="#90EE90", font=("Helvetica", 12))
        submit_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def submit(self):
        meal_time = self.meal_time_entry.get().strip()
        date = self.date_entry.get().strip()
        meal_type = self.type_entry.get().strip()

        if not meal_time or not date or not meal_type:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO meals (meal_time, date, meal_type) VALUES (?, ?, ?)", (meal_time, date, meal_type))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Meal added successfully!")
        self.meal_time_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.display_entries()

    def display_entries(self):
        """Display all saved meals."""
        display_frame = tk.Frame(self.top, bg="#f0f8ff")
        display_frame.pack(pady=10, padx=20)

        tk.Label(display_frame, text="Your Meals:", font=("Helvetica", 14, "bold"), bg="#f0f8ff").pack()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT meal_time, date, meal_type FROM meals")
        meals = cursor.fetchall()
        cursor.close()
        conn.close()

        for meal in meals:
            tk.Label(display_frame, text=f"Time: {meal[0]}, Date: {meal[1]}, Type: {meal[2]}", bg="#f0f8ff").pack(anchor='w')

# ----------------- RecipePlanner Class -----------------

class RecipePlanner(Planner):
    """Class for Recipe Planner functionality."""

    def __init__(self, root):
        super().__init__(root, "Recipe Planner")
        self.display_entries()

    def create_form(self):
        frame = tk.Frame(self.top, bg="#e6f7ff", padx=20, pady=20, bd=2, relief=tk.RAISED)
        frame.pack(pady=20, padx=20)

        tk.Label(frame, text="Recipe Name:", bg="#e6f7ff", font=("Helvetica", 12)).grid(row=0, column=0, pady=5, sticky='e')
        self.recipe_name_entry = tk.Entry(frame, width=30)
        self.recipe_name_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Ingredients:", bg="#e6f7ff", font=("Helvetica", 12)).grid(row=1, column=0, pady=5, sticky='e')
        self.ingredients_entry = tk.Text(frame, height=5, width=30)
        self.ingredients_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Description:", bg="#e6f7ff", font=("Helvetica", 12)).grid(row=2, column=0, pady=5, sticky='e')
        self.description_entry = tk.Text(frame, height=5, width=30)
        self.description_entry.grid(row=2, column=1, pady=5)

        submit_btn = tk.Button(frame, text="Add Recipe", command=self.submit, bg="#90EE90", font=("Helvetica", 12))
        submit_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def submit(self):
        name = self.recipe_name_entry.get().strip()
        ingredients = self.ingredients_entry.get("1.0", tk.END).strip()
        description = self.description_entry.get("1.0", tk.END).strip()

        if not name or not ingredients or not description:
            messagebox.showerror("Input Error", "All fields must be filled out.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO recipes (name, ingredients, description) VALUES (?, ?, ?)", (name, ingredients, description))
        conn.commit()
        cursor.close()
        conn.close()

        messagebox.showinfo("Success", "Recipe added successfully!")
        self.recipe_name_entry.delete(0, tk.END)
        self.ingredients_entry.delete("1.0", tk.END)
        self.description_entry.delete("1.0", tk.END)
        self.display_entries()

    def display_entries(self):
        """Display all saved recipes."""
        display_frame = tk.Frame(self.top, bg="#f0f8ff")
        display_frame.pack(pady=10, padx=20)

        tk.Label(display_frame, text="Your Recipes:", font=("Helvetica", 14, "bold"), bg="#f0f8ff").pack()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, ingredients, description FROM recipes")
        recipes = cursor.fetchall()
        cursor.close()
        conn.close()

        for recipe in recipes:
            tk.Label(display_frame, text=f"Name: {recipe[0]}, Ingredients: {recipe[1]}", bg="#f0f8ff").pack(anchor='w')

# ----------------- GroceryItem Class -----------------

class GroceryItem:
    """Class representing a grocery item."""
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def display_item(self):
        return f"{self.name}\n₹{self.price:.2f}"

# ----------------- GroceryStore Class -----------------

class GroceryStore:
    """Class for Grocery Store functionality."""

    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Grocery Store")
        self.top.geometry("900x600")
        self.top.config(bg="#f0f8ff")
        self.create_grocery_store()

    def create_grocery_store(self):
        # Scrollable Frame Setup
        container = tk.Frame(self.top, bg="#f0f8ff")
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, bg="#f0f8ff")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f8ff")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Fetch grocery items from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM groceries")
        groceries = cursor.fetchall()
        cursor.close()
        conn.close()

        # Display products in grid
        columns = 5
        for index, grocery in enumerate(groceries):
            row = index // columns
            col = index % columns
            item_frame = tk.Frame(scrollable_frame, bg="#f0f8ff", padx=10, pady=10, bd=1, relief=tk.RAISED)
            item_frame.grid(row=row, column=col, padx=10, pady=10)

            # Product Name and Price
            tk.Label(item_frame, text=grocery[1], font=("Helvetica", 10, "bold"), bg="#f0f8ff").pack()
            tk.Label(item_frame, text=f"₹{grocery[2]:.2f}", font=("Helvetica", 10), bg="#f0f8ff").pack(pady=5)

            # Add to Cart Button
            add_btn = tk.Button(item_frame, text="Add to Cart", command=lambda g=grocery: self.add_to_cart(g), bg="#90EE90")
            add_btn.pack()

    def add_to_cart(self, grocery):
        """Add selected grocery item to the cart."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT quantity FROM cart WHERE grocery_id=?", (grocery[0],))
        result = cursor.fetchone()
        if result:
            # If item already in cart, increment quantity
            new_quantity = result[0] + 1
            cursor.execute("UPDATE cart SET quantity=? WHERE grocery_id=?", (new_quantity, grocery[0]))
        else:
            # Else, insert new item
            cursor.execute("INSERT INTO cart (grocery_id, quantity) VALUES (?, ?)", (grocery[0], 1))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Success", f"{grocery[1]} has been added to your cart.")

# ----------------- Cart Class -----------------

class Cart:
    """Class for Cart functionality."""

    def __init__(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Cart")
        self.top.geometry("600x500")
        self.top.config(bg="#f0f8ff")
        self.create_cart()

    def create_cart(self):
        # Frame Setup
        frame = tk.Frame(self.top, bg="#f0f8ff", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # Cart Items Label
        tk.Label(frame, text="Your Cart", font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(pady=10)

        # Scrollable Frame for Cart Items
        canvas = tk.Canvas(frame, bg="#f0f8ff")
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#f0f8ff")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Fetch cart items from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT groceries.name, groceries.price, cart.quantity
            FROM cart
            JOIN groceries ON cart.grocery_id = groceries.id
        """)
        cart_items = cursor.fetchall()
        cursor.close()
        conn.close()

        if not cart_items:
            tk.Label(scrollable_frame, text="Your cart is empty.", font=("Helvetica", 12), bg="#f0f8ff").pack()
            return

        # Display cart items
        for item in cart_items:
            item_frame = tk.Frame(scrollable_frame, bg="#f0f8ff", pady=5)
            item_frame.pack(fill=tk.X)

            tk.Label(item_frame, text=item[0], font=("Helvetica", 12), bg="#f0f8ff", width=30, anchor='w').pack(side=tk.LEFT)
            tk.Label(item_frame, text=f"₹{item[1]:.2f} x {item[2]}", font=("Helvetica", 12), bg="#f0f8ff").pack(side=tk.LEFT, padx=10)
            remove_btn = tk.Button(item_frame, text="Remove", command=lambda n=item[0]: self.remove_item(n), bg="#FF6347")
            remove_btn.pack(side=tk.RIGHT)

    def remove_item(self, name):
        """Remove item from the cart."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cart.id FROM cart
            JOIN groceries ON cart.grocery_id = groceries.id
            WHERE groceries.name=?
        """, (name,))
        result = cursor.fetchone()
        if result:
            cursor.execute("DELETE FROM cart WHERE id=?", (result[0],))
            conn.commit()
            messagebox.showinfo("Removed", f"{name} has been removed from your cart.")
            self.top.destroy()
            Cart(self.top.master)  # Refresh cart view
        cursor.close()
        conn.close()

# ----------------- MealPlannerApp Class -----------------

class MealPlannerApp:
    """Main Application Class."""

    def __init__(self, root):
        self.root = root
        self.root.title("Meal Planner App")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f8ff")
        self.create_homepage()

    def create_homepage(self):
        frame = tk.Frame(self.root, bg="#e6f7ff", padx=20, pady=20, bd=2, relief=tk.RAISED)
        frame.pack(pady=50, padx=50, fill=tk.BOTH, expand=True)

        # Welcome Label
        tk.Label(frame, text="Welcome to Zoozoo Meal Planner!", font=("Helvetica", 18, "bold"), fg="#2F4F4F", bg="#e6f7ff").pack(pady=20)

        # Navigation Buttons
        buttons = [
            ("Meal Planner", self.open_meal_planner),
            ("Recipe Planner", self.open_recipe_planner),
            ("Grocery Store", self.open_grocery_store),
            ("Cart", self.open_cart)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(frame, text=text, command=command, bg="#add8e6", font=("Helvetica", 14), width=20, height=2, bd=3, relief=tk.RAISED)
            btn.pack(pady=10)

        # Discounts Section
        discounts = [("Vegetables", "50% Off"), ("General Items", "40% Off"), ("Fruits", "30% Off")]
        discount_frame = tk.Frame(self.root, bg="#ffcccb", padx=10, pady=10, bd=2, relief=tk.RAISED)
        discount_frame.pack(pady=10, padx=20, fill=tk.X)

        tk.Label(discount_frame, text="Discounts:", font=("Helvetica", 14, "bold"), bg="#ffcccb").pack(side=tk.LEFT, padx=10)
        for item, discount in discounts:
            tk.Label(discount_frame, text=f"{item}: {discount}", font=("Helvetica", 12), bg="#ffcccb").pack(side=tk.LEFT, padx=5)

        # New Items Section
        new_items = ["Fresh Fruits", "Dairy Products", "Organic Vegetables"]
        new_items_frame = tk.Frame(self.root, bg="#c1e1ff", padx=10, pady=10, bd=2, relief=tk.RAISED)
        new_items_frame.pack(pady=10, padx=20, fill=tk.X)

        tk.Label(new_items_frame, text="New Items:", font=("Helvetica", 14, "bold"), bg="#c1e1ff").pack(side=tk.LEFT, padx=10)
        for item in new_items:
            tk.Label(new_items_frame, text=item, font=("Helvetica", 12), bg="#c1e1ff").pack(side=tk.LEFT, padx=5)

    def open_meal_planner(self):
        MealPlanner(self.root)

    def open_recipe_planner(self):
        RecipePlanner(self.root)

    def open_grocery_store(self):
        GroceryStore(self.root)

    def open_cart(self):
        Cart(self.root)

# ----------------- Main Execution -----------------

if __name__ == "__main__":
    # Setup database and populate data if necessary
    if not os.path.exists('meal_planner.db'):
        setup_db()
        populate_groceries()
        populate_discounts()

    # Start the application
    root = tk.Tk()
    app = MealPlannerApp(root)
    root.mainloop()
