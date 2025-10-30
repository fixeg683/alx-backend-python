import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker for generating fake data
fake = Faker()

# Connect to the SQLite database (change if using PostgreSQL/MySQL)
conn = sqlite3.connect('airbnb_clone.db')
cursor = conn.cursor()

# Create tables if not exist (for local testing)
cursor.executescript('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    location TEXT,
    price_per_night REAL,
    host_id INTEGER,
    FOREIGN KEY (host_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    property_id INTEGER,
    check_in DATE,
    check_out DATE,
    total_amount REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (property_id) REFERENCES properties(id)
);

CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER,
    payment_date DATETIME,
    amount REAL,
    status TEXT,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
);

CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER,
    user_id INTEGER,
    rating INTEGER,
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES properties(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
''')

conn.commit()

# ---------- SEED DATA ----------
NUM_USERS = 20
NUM_PROPERTIES = 30
NUM_BOOKINGS = 40
NUM_PAYMENTS = 40
NUM_REVIEWS = 50

# --- USERS ---
users = []
for _ in range(NUM_USERS):
    name = fake.name()
    email = fake.unique.email()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    users.append(cursor.lastrowid)

# --- PROPERTIES ---
properties = []
for _ in range(NUM_PROPERTIES):
    name = fake.word().capitalize() + " Apartment"
    location = fake.city()
    price_per_night = round(random.uniform(40, 400), 2)
    host_id = random.choice(users)
    cursor.execute(
        "INSERT INTO properties (name, location, price_per_night, host_id) VALUES (?, ?, ?, ?)",
        (name, location, price_per_night, host_id)
    )
    properties.append(cursor.lastrowid)

# --- BOOKINGS ---
bookings = []
for _ in range(NUM_BOOKINGS):
    user_id = random.choice(users)
    property_id = random.choice(properties)
    check_in = fake.date_between(start_date="-3y", end_date="today")
    check_out = check_in + timedelta(days=random.randint(1, 10))
    total_amount = round(random.uniform(100, 1500), 2)
    cursor.execute('''
        INSERT INTO bookings (user_id, property_id, check_in, check_out, total_amount)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, property_id, check_in, check_out, total_amount))
    bookings.append(cursor.lastrowid)

# --- PAYMENTS ---
for booking_id in bookings:
    payment_date = fake.date_between(start_date="-3y", end_date="today")
    amount = round(random.uniform(100, 1500), 2)
    status = random.choice(["Completed", "Pending", "Failed"])
    cursor.execute('''
        INSERT INTO payments (booking_id, payment_date, amount, status)
        VALUES (?, ?, ?, ?)
    ''', (booking_id, payment_date, amount, status))

# --- REVIEWS ---
for _ in range(NUM_REVIEWS):
    property_id = random.choice(properties)
    user_id = random.choice(users)
    rating = random.randint(1, 5)
    comment = fake.sentence(nb_words=12)
    cursor.execute('''
        INSERT INTO reviews (property_id, user_id, rating, comment)
        VALUES (?, ?, ?, ?)
    ''', (property_id, user_id, rating, comment))

conn.commit()
conn.close()

print("✅ Database seeded successfully with sample data!")
