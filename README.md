# Movie Ticket Booking System

## Project Description
The Movie Ticket Booking System is a desktop-based application developed using Python and MySQL for managing movie ticket reservations efficiently. The system provides functionalities for adding movie details, storing customer information, booking tickets, calculating total ticket prices, and displaying booking records through an interactive graphical user interface.

## Features
- Add and manage movie details
- Store customer information
- Book movie tickets
- Automatic ticket price calculation
- View all booking records
- Interactive GUI using Tkinter
- MySQL database connectivity

## Technologies Used
- Python
- Tkinter
- MySQL
- MySQL Connector
- SQL

## Database Structure
The database contains the following tables:
- Movies
- Customers
- Bookings

Relational database concepts are used to maintain proper data management and connectivity between tables.

## Installation and Execution
### Step 1: Install Required Software
- Python
- MySQL Server

### Step 2: Install Required Python Package
```bash
pip install mysql-connector-python
```

### Step 3: Import Database
Import the provided SQL file into MySQL:
```text
movie_db.sql
```

### Step 4: Configure Database Credentials
Update the MySQL username and password inside the Python source code.

### Step 5: Run the Application
```bash
python movie_ticket_system.py
```


# Modules Included
### Movie Management
Allows users to add and manage movie details including title, genre, duration, show time, and ticket price.

### Customer Management
Stores customer details such as name, email, and phone number.

### Ticket Booking
Enables booking of movie tickets and automatically calculates total booking amount.

### Booking Records
Displays all booking information in a tabular format using Treeview.


# Output
The system provides:
- Graphical user interface for easy interaction
- Booking confirmation messages
- Real-time booking records display

 # Objectives
- To develop a database-driven movie ticket booking application
- To understand GUI development using Python
- To implement database connectivity using MySQL
- To perform CRUD operations efficiently

# Learning Outcomes
- Understanding relational database management
- Python GUI application development
- Database connectivity using MySQL Connector
- Implementation of booking management system

# Future Enhancements
- Online payment integration
- Seat selection feature
- User authentication system
- Email ticket confirmation
- Admin dashboard

## Author
Hema sri.G
