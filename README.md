# Reseller Store - Flask Web Application

A fully functional reseller website built with Flask, featuring product browsing, order management, and admin panel.

## 🚀 Features

### Customer Features
- **Product Browsing**: View all available products with images, descriptions, and prices
- **Order Placement**: Place orders with customer information and quantity selection
- **Responsive Design**: Modern, mobile-friendly interface

### Admin Features
- **Secure Login**: Session-based authentication system
- **Product Management**: Add, view, and delete products
- **Order Tracking**: View all customer orders with details
- **Dashboard Statistics**: Overview of products, orders, and revenue

## 🛠 Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: Bootstrap 5, Font Awesome
- **Templates**: Jinja2

## 📁 Project Structure

```
/reseller-site
├── app.py                 # Main Flask application
├── db.sqlite3            # SQLite database (auto-created)
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── templates/
    ├── home.html        # Homepage with product listing
    ├── login.html       # Admin login page
    ├── order.html       # Order placement form
    └── admin_dashboard.html  # Admin panel
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the website**:
   - Open your browser and go to: `http://localhost:5000`
   - Admin panel: `http://localhost:5000/login`

## 🔐 Default Admin Credentials

- **Username**: `admin`
- **Password**: `admin123`

## 📋 Database Schema

### Products Table
- `id` (Primary Key)
- `name` (Product name)
- `price` (Product price)
- `description` (Product description)
- `image_url` (Product image URL)
- `created_at` (Timestamp)

### Orders Table
- `id` (Primary Key)
- `customer_name` (Customer's full name)
- `customer_email` (Customer's email)
- `customer_phone` (Customer's phone number)
- `product_id` (Foreign key to products)
- `quantity` (Order quantity)
- `total_amount` (Total order amount)
- `order_date` (Order timestamp)

### Admin Table
- `id` (Primary Key)
- `username` (Admin username)
- `password` (Admin password)

## 🎯 How to Use

### For Customers
1. Visit the homepage to browse products
2. Click "Order Now" on any product
3. Fill in your details and quantity
4. Submit the order

### For Admins
1. Go to `/login` and use the default credentials
2. Access the admin dashboard
3. Add new products using the form
4. View and manage existing products
5. Monitor customer orders

## 🔧 Customization

### Adding Sample Products
The application comes with 5 sample products. You can:
- Add more products through the admin panel
- Modify the sample data in `app.py` (lines with `sample_products`)

### Styling
- All styling is done with Bootstrap 5
- Custom CSS is included in each template
- Modify the `<style>` sections in HTML files to customize appearance

### Database
- The SQLite database (`db.sqlite3`) is created automatically
- You can use any SQLite browser to view/edit the database directly

## 🛡️ Security Notes

- Change the default admin credentials in production
- Update the `secret_key` in `app.py` for production use
- Consider implementing password hashing for better security
- Add input validation and sanitization for production use

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile phones

## 🎨 Features Overview

- **Modern UI**: Clean, professional design with Bootstrap 5
- **Real-time Calculations**: Order totals update automatically
- **Flash Messages**: User-friendly notifications
- **Confirmation Dialogs**: Safe deletion with confirmation
- **Image Support**: Product images from URLs
- **Session Management**: Secure admin login/logout

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**:
   - Change the port in `app.py`: `app.run(debug=True, port=5001)`

2. **Database errors**:
   - Delete `db.sqlite3` and restart the application

3. **Template errors**:
   - Ensure all HTML files are in the `templates/` folder

4. **Import errors**:
   - Make sure all dependencies are installed: `pip install -r requirements.txt`

## 📞 Support

If you encounter any issues:
1. Check the console output for error messages
2. Verify all files are in the correct locations
3. Ensure Python and Flask are properly installed

---

**Happy Selling! 🛍️** 