import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('meal_planner.db')
    return conn

class MealPlannerApp:
    def _init_(self, root):
        self.root = root
        self.root.title("Meal Planner App")
        self.root.geometry("800x600")
        self.create_homepage()

    def create_homepage(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        meal_planner_btn = tk.Button(frame, text="Meal Planner", command=self.open_meal_planner)
        recipe_planner_btn = tk.Button(frame, text="Recipe Planner", command=self.open_recipe_planner)
        grocery_store_btn = tk.Button(frame, text="Grocery Store", command=self.open_grocery_store)
        cart_btn = tk.Button(frame, text="Cart", command=self.open_cart)

        meal_planner_btn.grid(row=0, column=0, padx=10)
        recipe_planner_btn.grid(row=0, column=1, padx=10)
        grocery_store_btn.grid(row=0, column=2, padx=10)
        cart_btn.grid(row=0, column=3, padx=10)

    def open_meal_planner(self):
        MealPlanner(self.root)

    def open_recipe_planner(self):
        RecipePlanner(self.root)

    def open_grocery_store(self):
        GroceryStore(self.root)

    def open_cart(self):
        Cart(self.root)

class MealPlanner:
    def _init_(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Meal Planner")
        self.create_meal_form()

    def create_meal_form(self):
        tk.Label(self.top, text="Meal Time:").grid(row=0, column=0)
        self.meal_time_entry = tk.Entry(self.top)
        self.meal_time_entry.grid(row=0, column=1)

        tk.Label(self.top, text="Date (YYYY-MM-DD):").grid(row=1, column=0)
        self.date_entry = tk.Entry(self.top)
        self.date_entry.grid(row=1, column=1)

        tk.Label(self.top, text="Type (Breakfast/Lunch/Dinner):").grid(row=2, column=0)
        self.type_entry = tk.Entry(self.top)
        self.type_entry.grid(row=2, column=1)

        submit_btn = tk.Button(self.top, text="Submit", command=self.submit_meal)
        submit_btn.grid(row=3, column=0, columnspan=2)

    def submit_meal(self):
        meal_data = (
            self.meal_time_entry.get(),
            self.date_entry.get(),
            self.type_entry.get()
        )
        self.save_meal_to_db(meal_data)
        messagebox.showinfo("Success", "Meal added successfully!")

    def save_meal_to_db(self, meal_data):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO meals (meal_time, date, meal_type) VALUES (?, ?, ?)", meal_data)
        conn.commit()
        cursor.close()
        conn.close()

class RecipePlanner:
    def _init_(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Recipe Planner")
        self.create_recipe_form()

    def create_recipe_form(self):
        tk.Label(self.top, text="Recipe Name:").grid(row=0, column=0)
        self.recipe_name_entry = tk.Entry(self.top)
        self.recipe_name_entry.grid(row=0, column=1)

        tk.Label(self.top, text="Ingredients:").grid(row=1, column=0)
        self.ingredients_entry = tk.Text(self.top, height=5, width=40)
        self.ingredients_entry.grid(row=1, column=1)

        tk.Label(self.top, text="Description:").grid(row=2, column=0)
        self.description_entry = tk.Text(self.top, height=5, width=40)
        self.description_entry.grid(row=2, column=1)

        submit_btn = tk.Button(self.top, text="Submit", command=self.submit_recipe)
        submit_btn.grid(row=3, column=0, columnspan=2)

    def submit_recipe(self):
        recipe_data = (
            self.recipe_name_entry.get(),
            self.ingredients_entry.get("1.0", tk.END).strip(),
            self.description_entry.get("1.0", tk.END).strip()
        )
        self.save_recipe_to_db(recipe_data)
        messagebox.showinfo("Success", "Recipe added successfully!")

    def save_recipe_to_db(self, recipe_data):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO recipes (name, ingredients, description) VALUES (?, ?, ?)", recipe_data)
        conn.commit()
        cursor.close()
        conn.close()

class GroceryStore:
    def _init_(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Grocery Store")
        self.display_grocery_items()

    def display_grocery_items(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price, image_path FROM groceries")
        groceries = cursor.fetchall()

        for grocery in groceries:
            frame = tk.Frame(self.top)
            frame.pack(side=tk.TOP, fill=tk.X)

            img_path = grocery[3]
            img = tk.PhotoImage(file=img_path) if os.path.exists(img_path) else tk.PhotoImage()
            img_label = tk.Label(frame, image=img)
            img_label.image = img  # Keep a reference
            img_label.pack(side=tk.LEFT)

            name_label = tk.Label(frame, text=grocery[1])
            name_label.pack(side=tk.LEFT)

            price_label = tk.Label(frame, text=f"${grocery[2]:.2f}")
            price_label.pack(side=tk.LEFT)

            add_btn = tk.Button(frame, text="Add to Cart", command=lambda g=grocery: self.add_to_cart(g))
            add_btn.pack(side=tk.LEFT)

        cursor.close()
        conn.close()

    def add_to_cart(self, grocery):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cart (grocery_id, quantity) VALUES (?, ?)", (grocery[0], 1))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Added to Cart", f"{grocery[1]} added to cart.")

class Cart:
    def _init_(self, root):
        self.top = tk.Toplevel(root)
        self.top.title("Cart")
        self.display_cart_items()

    def display_cart_items(self):
        tk.Label(self.top, text="Your Cart Items:").pack()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT groceries.name, groceries.price, cart.quantity FROM cart JOIN groceries ON cart.grocery_id = groceries.id")
        items = cursor.fetchall()

        total_price = 0
        for item in items:
            item_frame = tk.Frame(self.top)
            item_frame.pack(fill=tk.X)

            name_label = tk.Label(item_frame, text=item[0], font=("Arial", 12))
            name_label.pack(side=tk.LEFT, padx=10)

            price_label = tk.Label(item_frame, text=f"${item[1]:.2f}", font=("Arial", 12))
            price_label.pack(side=tk.LEFT, padx=10)

            quantity_label = tk.Label(item_frame, text=f"x{item[2]}", font=("Arial", 12))
            quantity_label.pack(side=tk.LEFT, padx=10)

            total_price += item[1] * item[2]

        total_label = tk.Label(self.top, text=f"Total: ${total_price:.2f}", font=("Arial", 16, "bold"))
        total_label.pack(pady=10)

        checkout_btn = tk.Button(self.top, text="Checkout", command=self.checkout)
        checkout_btn.pack(pady=20)

        cursor.close()
        conn.close()

    def checkout(self):
        messagebox.showinfo("Checkout", "Proceed to checkout.")

if __name__ == "_main_":
    root = tk.Tk()
    app = MealPlannerApp(root)
    root.mainloop()