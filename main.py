import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


# Initialize Database
def initialize_db():
    connection = sqlite3.connect("invoice_generator.db")
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            contact TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            date TEXT NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (invoice_id) REFERENCES invoices(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    connection.commit()
    connection.close()


# Save client to database
def save_client(name, address, contact):
    connection = sqlite3.connect("invoice_generator.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO clients (name, address, contact) VALUES (?, ?, ?)", (name, address, contact))
    connection.commit()
    connection.close()


# Save product to database
def save_product(name, price):
    connection = sqlite3.connect("invoice_generator.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
    connection.commit()
    connection.close()


# Fetch all clients
def fetch_clients():
    connection = sqlite3.connect("invoice_generator.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    connection.close()
    return clients


# Fetch all products
def fetch_products():
    connection = sqlite3.connect("invoice_generator.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    connection.close()
    return products


# Generate Invoice PDF
def generate_invoice_pdf(invoice_id, client_name, client_address, items, total):
    filename = f"invoice_{invoice_id}.pdf"
    pdf = canvas.Canvas(filename, pagesize=letter)
    pdf.setFont("Helvetica", 12)

    pdf.drawString(100, 750, f"Invoice ID: {invoice_id}")
    pdf.drawString(100, 730, f"Client: {client_name}")
    pdf.drawString(100, 710, f"Address: {client_address}")
    pdf.drawString(100, 690, f"Date: {datetime.now().strftime('%Y-%m-%d')}")

    y_position = 650
    pdf.drawString(100, y_position, "Items:")
    y_position -= 20
    pdf.drawString(100, y_position, "----------------------------------")
    y_position -= 20

    for item in items:
        pdf.drawString(100, y_position, f"{item[0]} - {item[1]} x {item[2]} = ${item[3]:.2f}")
        y_position -= 20

    pdf.drawString(100, y_position - 20, f"Total: ${total:.2f}")
    pdf.save()
    messagebox.showinfo("Success", f"Invoice saved as {filename}")


# Initialize Database
initialize_db()

# Placeholder GUI - To be expanded
root = tk.Tk()
root.title("Invoice Generator")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

tk.Label(frame, text="Invoice Generator", font=("Arial", 16)).pack()
tk.Label(frame, text="(GUI under development)").pack()

root.mainloop()
