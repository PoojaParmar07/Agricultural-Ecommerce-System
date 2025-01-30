# Jyoti Agro - E-commerce for Seeds and Fertilizers

## Overview
Jyoti Agro is an e-commerce platform designed to sell agricultural seeds and fertilizers. The project is part of a final-year academic submission, incorporating various features such as product management, user authentication, membership plans, and order handling with multiple payment options.

## Features
- **User Authentication**:Registration and login system for both users and admins.
- **Product Management**: Different units and prices for seeds and fertilizers.
- **Membership System**: Gold plan with different benefits.
- **Shopping Cart**: Add products to the cart.
- **Order Processing**: Supports online payments and Cash on Delivery (COD).
- **Bill Generation**: Generates bills for completed orders.

## Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MySQL 


## Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/jyoti-agro.git
   cd jyoti-agro
   ```
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Database** (Ensure MySQL is running in XAMPP)
   - Update `settings.py` with database credentials
   - Apply migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```
4. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```
5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```
6. **Access the Application**
   - User Dashboard: `http://127.0.0.1:8000/`
   - Admin Panel: `http://127.0.0.1:8000/admin/dashboard`

## License
This project is for educational purposes only.



