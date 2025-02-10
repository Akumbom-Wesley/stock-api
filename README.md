# Stock Management API

A Django-based API designed to manage stock, inventory, purchases, transactions, and suppliers. This project is intended to track products, monitor stock levels, and process purchase orders, transactions, and product movements.

## Features

- **User Management**: Allows authentication for users and suppliers with JWT-based authentication.
- **Product Management**: Manage products, categories, and inventory stock levels.
- **Purchase Order Management**: Track purchase orders and their items.
- **Transaction Management**: Record and track stock movements such as sales, restocks, and adjustments.
- **Supplier Management**: Manage supplier information.
- **Audit**: Track changes to stock and transactions.

## Technologies Used

- **Django**: Web framework for building the API.
- **Django Rest Framework (DRF)**: For building RESTful APIs.
- **JWT Authentication**: For securing endpoints and handling user login and registration.
- **SQLite** (default) or PostgreSQL: For database management.
- **Docker** (optional): For containerization.

## Setup

### Prerequisites

- Python 3.x
- Django 4.x
- Django Rest Framework
- PostgreSQL (optional, SQLite by default)

### Clone the repository

```bash
git clone https://github.com/yourusername/stock-management-api.git
cd stock-management-api

## Setup Instructions

### Create and activate a virtual environment

Using `venv`:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```

The server should now be running on http://127.0.0.1:8000/.