import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date

# === DATABASE CONNECTION ===
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # 👈 your MySQL username
        password="131529", # 👈 your MySQL password
        database="movie_db"
    )

# === MAIN WINDOW ===
root = tk.Tk()
root.title("🎟️ Movie Ticket Booking System")
root.geometry("1200x700")
root.configure(bg="#ececec")

title_label = tk.Label(root, text="🎬 Movie Ticket Booking System", font=("Helvetica", 24, "bold"), bg="#ececec", fg="#333")
title_label.pack(pady=20)

# === FRAMES ===
movie_frame = tk.LabelFrame(root, text="Add / Manage Movies", padx=10, pady=10, bg="#f8f8f8", font=("Arial", 12, "bold"))
movie_frame.place(x=20, y=100, width=500, height=400)

booking_frame = tk.LabelFrame(root, text="Book Tickets", padx=10, pady=10, bg="#f8f8f8", font=("Arial", 12, "bold"))
booking_frame.place(x=540, y=100, width=640, height=400)

table_frame = tk.LabelFrame(root, text="Booking Records", bg="white", font=("Arial", 12, "bold"))
table_frame.place(x=20, y=520, width=1160, height=160)

# === MOVIE FORM ===
tk.Label(movie_frame, text="Title:", bg="#f8f8f8").grid(row=0, column=0, sticky="w")
movie_title = tk.Entry(movie_frame, width=30)
movie_title.grid(row=0, column=1, pady=5)

tk.Label(movie_frame, text="Genre:", bg="#f8f8f8").grid(row=1, column=0, sticky="w")
movie_genre = tk.Entry(movie_frame, width=30)
movie_genre.grid(row=1, column=1, pady=5)

tk.Label(movie_frame, text="Duration (min):", bg="#f8f8f8").grid(row=2, column=0, sticky="w")
movie_duration = tk.Entry(movie_frame, width=30)
movie_duration.grid(row=2, column=1, pady=5)

tk.Label(movie_frame, text="Show Time (HH:MM):", bg="#f8f8f8").grid(row=3, column=0, sticky="w")
movie_show = tk.Entry(movie_frame, width=30)
movie_show.grid(row=3, column=1, pady=5)

tk.Label(movie_frame, text="Ticket Price:", bg="#f8f8f8").grid(row=4, column=0, sticky="w")
movie_price = tk.Entry(movie_frame, width=30)
movie_price.grid(row=4, column=1, pady=5)

def add_movie():
    if not movie_title.get():
        messagebox.showwarning("Input Error", "Please enter a movie title.")
        return
    db = connect_db()
    cur = db.cursor()
    cur.execute("INSERT INTO movies (title, genre, duration, show_time, ticket_price) VALUES (%s,%s,%s,%s,%s)",
                (movie_title.get(), movie_genre.get(), movie_duration.get(), movie_show.get(), movie_price.get()))
    db.commit()
    db.close()
    messagebox.showinfo("Success", "Movie added successfully!")
    clear_movie()

def clear_movie():
    movie_title.delete(0, tk.END)
    movie_genre.delete(0, tk.END)
    movie_duration.delete(0, tk.END)
    movie_show.delete(0, tk.END)
    movie_price.delete(0, tk.END)

tk.Button(movie_frame, text="Add Movie", command=add_movie, bg="#4CAF50", fg="white", width=15).grid(row=5, column=0, pady=10)
tk.Button(movie_frame, text="Clear", command=clear_movie, bg="#9c9c9c", fg="white", width=15).grid(row=5, column=1, pady=10)

# === BOOKING SECTION ===
tk.Label(booking_frame, text="Customer Name:", bg="#f8f8f8").grid(row=0, column=0, sticky="w")
cust_name = tk.Entry(booking_frame, width=25)
cust_name.grid(row=0, column=1, pady=5)

tk.Label(booking_frame, text="Email:", bg="#f8f8f8").grid(row=1, column=0, sticky="w")
cust_email = tk.Entry(booking_frame, width=25)
cust_email.grid(row=1, column=1, pady=5)

tk.Label(booking_frame, text="Phone:", bg="#f8f8f8").grid(row=2, column=0, sticky="w")
cust_phone = tk.Entry(booking_frame, width=25)
cust_phone.grid(row=2, column=1, pady=5)

tk.Label(booking_frame, text="Select Movie:", bg="#f8f8f8").grid(row=3, column=0, sticky="w")

def fetch_movies():
    db = connect_db()
    cur = db.cursor()
    cur.execute("SELECT title FROM movies")
    movies = [row[0] for row in cur.fetchall()]
    db.close()
    return movies

movie_combo = ttk.Combobox(booking_frame, values=fetch_movies(), width=22)
movie_combo.grid(row=3, column=1, pady=5)

tk.Label(booking_frame, text="Seats:", bg="#f8f8f8").grid(row=4, column=0, sticky="w")
cust_seats = tk.Entry(booking_frame, width=25)
cust_seats.grid(row=4, column=1, pady=5)

def book_ticket():
    if not cust_name.get() or not movie_combo.get() or not cust_seats.get():
        messagebox.showwarning("Missing Info", "Please fill all booking details!")
        return

    db = connect_db()
    cur = db.cursor()

    # Insert or find customer
    cur.execute("INSERT INTO customers (name, email, phone) VALUES (%s,%s,%s)", (cust_name.get(), cust_email.get(), cust_phone.get()))
    cust_id = cur.lastrowid

    # Find movie details
    cur.execute("SELECT movie_id, ticket_price FROM movies WHERE title=%s", (movie_combo.get(),))
    movie = cur.fetchone()
    if not movie:
        messagebox.showerror("Error", "Selected movie not found!")
        db.close()
        return
    movie_id, price = movie
    total = float(price) * int(cust_seats.get())

    # Insert booking
    cur.execute("INSERT INTO bookings (customer_id, movie_id, seats, booking_date, total_price) VALUES (%s,%s,%s,%s,%s)",
                (cust_id, movie_id, cust_seats.get(), date.today(), total))
    db.commit()
    db.close()
    messagebox.showinfo("Success", f"Booking confirmed!\nTotal Price: ₹{total}")
    fetch_data()

def fetch_data():
    for i in booking_table.get_children():
        booking_table.delete(i)
    db = connect_db()
    cur = db.cursor()
    cur.execute("""
        SELECT b.booking_id, c.name, m.title, b.seats, b.booking_date, b.total_price
        FROM bookings b
        JOIN customers c ON b.customer_id = c.customer_id
        JOIN movies m ON b.movie_id = m.movie_id
    """)
    for row in cur.fetchall():
        booking_table.insert("", tk.END, values=row)
    db.close()

tk.Button(booking_frame, text="Book Ticket", bg="#2196F3", fg="white", width=20, command=book_ticket).grid(row=5, column=0, pady=20)
tk.Button(booking_frame, text="Show All Bookings", bg="#4CAF50", fg="white", width=20, command=fetch_data).grid(row=5, column=1, pady=20)

# === BOOKING TABLE ===
columns = ("Booking ID", "Customer", "Movie", "Seats", "Date", "Total")
booking_table = ttk.Treeview(table_frame, columns=columns, show="headings")

for col in columns:
    booking_table.heading(col, text=col)
    booking_table.column(col, width=180, anchor="center")

booking_table.pack(fill="both", expand=True)

# Start GUI
root.mainloop()
