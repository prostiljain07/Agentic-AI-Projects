import sqlite3
from pathlib import Path
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("en_IN")

# --------------------------------------------------------------------
# Database Location
# --------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "data" / "sales.db"

# Create the data folder if it doesn't exist
DB_PATH.parent.mkdir(exist_ok=True)

# --------------------------------------------------------------------
# Connect to SQLite
# --------------------------------------------------------------------

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (

    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,

    first_name TEXT NOT NULL,

    last_name TEXT NOT NULL,

    gender TEXT,

    age INTEGER,

    city TEXT,

    state TEXT,

    country TEXT,

    email TEXT UNIQUE,

    phone TEXT,

    join_date DATE

);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (

    product_id INTEGER PRIMARY KEY AUTOINCREMENT,

    product_name TEXT NOT NULL,

    category TEXT,

    brand TEXT,

    price REAL,

    stock INTEGER

);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (

    order_id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_id INTEGER,

    order_date DATE,

    payment_method TEXT,

    order_status TEXT,

    FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id)

);
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (

    item_id INTEGER PRIMARY KEY AUTOINCREMENT,

    order_id INTEGER,

    product_id INTEGER,

    quantity INTEGER,

    unit_price REAL,

    discount REAL,

    FOREIGN KEY(order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY(product_id)
        REFERENCES products(product_id)

);
""")

conn.commit()

print("Database created successfully!")


def insert_customers(cursor, n=500):

    print(f"Inserting {n} customers...")

    for _ in range(n):

        first = fake.first_name()
        last = fake.last_name()

        cursor.execute("""
        INSERT INTO customers
        (
            first_name,
            last_name,
            gender,
            age,
            city,
            state,
            country,
            email,
            phone,
            join_date
        )
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        (
            first,
            last,
            random.choice(["Male","Female"]),
            random.randint(18,70),
            fake.city(),
            fake.state(),
            "India",
            fake.unique.email(),
            fake.phone_number(),
            fake.date_between(start_date="-5y", end_date="today")
        ))

categories = {

    "Electronics": [
        "Laptop","Keyboard","Mouse","Monitor","Headphones",
        "Smartphone","Tablet","Printer","SSD","Webcam"
    ],

    "Clothing": [
        "Shirt","Jeans","Jacket","Shoes","T-Shirt",
        "Sweater","Shorts","Cap"
    ],

    "Home Appliances":[
        "Mixer","Microwave","Refrigerator",
        "Vacuum Cleaner","Iron","Fan"
    ],

    "Furniture":[
        "Chair","Table","Desk","Sofa",
        "Cupboard","Bookshelf"
    ],

    "Sports":[
        "Football","Cricket Bat","Basketball",
        "Tennis Racket","Yoga Mat"
    ],

    "Books":[
        "Python Guide","SQL Handbook",
        "AI Basics","Machine Learning",
        "Data Science"
    ],

    "Beauty":[
        "Face Wash","Shampoo",
        "Perfume","Body Lotion"
    ],

    "Grocery":[
        "Rice","Sugar","Coffee",
        "Tea","Milk","Olive Oil"
    ]
}

def insert_products(cursor, n=200):

    print(f"Inserting {n} products...")

    brands = [
        "Samsung",
        "Apple",
        "Sony",
        "Dell",
        "HP",
        "Nike",
        "Adidas",
        "LG",
        "Philips",
        "Puma"
    ]

    for _ in range(n):

        category = random.choice(list(categories.keys()))

        name = random.choice(categories[category])

        cursor.execute("""
        INSERT INTO products
        (
            product_name,
            category,
            brand,
            price,
            stock
        )
        VALUES (?,?,?,?,?)
        """,
        (
            name,
            category,
            random.choice(brands),
            round(random.uniform(100,50000),2),
            random.randint(10,500)
        ))

def insert_orders(cursor, n=3000):

    print(f"Inserting {n} orders...")

    for _ in range(n):

        cursor.execute("""
        INSERT INTO orders
        (
            customer_id,
            order_date,
            payment_method,
            order_status
        )
        VALUES (?,?,?,?)
        """,
        (
            random.randint(1,500),

            fake.date_between(start_date="-2y", end_date="today"),

            random.choice([
                "Credit Card",
                "Debit Card",
                "UPI",
                "Cash",
                "Net Banking"
            ]),

            random.choice([
                "Delivered",
                "Cancelled",
                "Returned",
                "Processing"
            ])
        ))


def insert_customers(cursor, n=500):

    print(f"Inserting {n} customers...")

    for _ in range(n):

        first = fake.first_name()
        last = fake.last_name()

        cursor.execute("""
        INSERT INTO customers
        (
            first_name,
            last_name,
            gender,
            age,
            city,
            state,
            country,
            email,
            phone,
            join_date
        )
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        (
            first,
            last,
            random.choice(["Male","Female"]),
            random.randint(18,70),
            fake.city(),
            fake.state(),
            "India",
            fake.unique.email(),
            fake.phone_number(),
            fake.date_between(start_date="-5y", end_date="today")
        ))

def insert_order_items(cursor):

    print("Creating order items...")

    item_count = 0

    for order_id in range(1,3001):

        number_of_products = random.randint(1,5)

        for _ in range(number_of_products):

            product = random.randint(1,200)

            quantity = random.randint(1,4)

            price = round(random.uniform(100,50000),2)

            discount = random.choice([0,5,10,15,20])

            cursor.execute("""
            INSERT INTO order_items
            (
                order_id,
                product_id,
                quantity,
                unit_price,
                discount
            )
            VALUES (?,?,?,?,?)
            """,
            (
                order_id,
                product,
                quantity,
                price,
                discount
            ))

            item_count += 1

    print(f"{item_count} order items inserted.")



insert_customers(cursor)

insert_products(cursor)

insert_orders(cursor)

insert_order_items(cursor)

conn.commit()

conn.close()

print("sales.db created successfully!")
