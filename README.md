## 🎥 Demo Video

https://drive.google.com/file/d/16kJIUtKjluFXT8p0ze2LMEWg5tgubHTq/view?usp=sharing


# Vikmo Sales Order & Inventory Management System

##  Project Overview

This project is a backend system built using Django and Django REST Framework for managing products, inventory, dealers, and sales orders.

It simulates a real-world B2B auto parts distribution platform where:

* Admin manages products and inventory
* Dealers place orders
* System validates stock and updates inventory automatically

---

##  Features Implemented

###  Product Management

* Create, update, delete products
* Unique SKU for each product
* Product listing with stock information

###  Inventory Management

* One-to-one relationship with product
* Tracks available stock
* Manual updates via admin panel
* Optional API for inventory management (bonus)

###  Dealer Management

* Create and manage dealers
* Each dealer can have multiple orders

###  Order Management

* Create draft orders
* Add multiple items (OrderItems)
* Auto-calculation of totals

###  Order Status Flow

* Draft → Confirmed → Delivered
* Draft: Editable, no stock impact
* Confirmed: Stock deducted, locked
* Delivered: Final state

###  Stock Validation (Critical)

* Prevents ordering more than available stock
* Validates before confirming order
* Shows clear error message for insufficient stock

###  Auto Calculations

* line_total = quantity × unit_price
* total_amount = sum of all line items
* order_number auto-generated (ORD-YYYYMMDD-XXXX)

---

## 🛠 Tech Stack

* Python 3.10+
* Django 4.2
* Django REST Framework
* SQLite (can be switched to PostgreSQL)

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repo-link>
cd vikmo_assignment
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Server

```bash
python manage.py runserver
```

---

##  API Endpoints

###  Products

* GET `/api/products/`
* POST `/api/products/`
* PUT `/api/products/{id}/`
* DELETE `/api/products/{id}/`

---

###  Dealers

* GET `/api/dealers/`
* POST `/api/dealers/`

---

###  Orders

* GET `/api/orders/`
* POST `/api/orders/`
* POST `/api/orders/{id}/confirm/`
* POST `/api/orders/{id}/deliver/`

---

###  Inventory (Bonus)

* GET `/api/inventory/`
* PUT `/api/inventory/{id}/`

---

##  Sample API Requests

### Create Product

```json
{
  "name": "Brake Pad",
  "sku": "BP001",
  "price": 500
}
```

---

### Create Dealer

```json
{
  "name": "ABC Motors",
  "email": "abc@gmail.com",
  "phone": "9999999999"
}
```

---

### Create Order

```json
{
  "dealer": 1,
  "items": [
    {
      "product": 1,
      "quantity": 10
    }
  ]
}
```

---

### Confirm Order

```
POST /api/orders/1/confirm/
```

---

##  Test Scenarios

###  Successful Order Flow

1. Create product
2. Add inventory (100 units)
3. Create dealer
4. Create order (10 units)
5. Confirm → stock reduces to 90
6. Deliver → order completed

---

###  Insufficient Stock

* Try ordering more than available stock
* System returns error:

```
Insufficient stock for Brake Pad. Available: X, Requested: Y
```

---

###  Invalid Status Transition

* Cannot confirm already confirmed order
* Cannot edit confirmed/delivered order

---

##  Design Decisions

* **OneToOne (Product → Inventory):** ensures single stock record per product
* **ForeignKey (Order → Dealer):** supports multiple orders per dealer
* **PROTECT on Product in OrderItem:** prevents deleting used products
* **transaction.atomic():** ensures safe stock updates
* **Unit price stored in OrderItem:** preserves historical pricing

---

##  Project Structure

```
vikmo_assignment/
│── manage.py
│── requirements.txt
│── README.md
│
├── vikmo_project/
│   ├── settings.py
│   ├── urls.py
│
├── core/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
```

---

##  Assumptions

* Each product has one inventory record
* Inventory managed by admin
* Orders cannot be modified after confirmation
* Price is fixed at time of order

---

##  Bonus Features Implemented

* Inventory API
* Swagger UI (`/swagger/`)
* Filtering support
* Clean REST API structure

---

##  Author

Bhuvan GR
