# Flask POS System

A simple web-based Point of Sale (POS) system for a single shop built with Flask.

## Features

- **Product Management**: Complete CRUD operations with stock tracking
- **Sales Recording**: Automatic price calculation and inventory deduction
- **Repair Job Tracking**: Customer details, device info, and status updates
- **Dashboard**: Daily sales totals and low-stock alerts (under 5 items)

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and navigate to `http://127.0.0.1:5000`

## Usage

### Product Management
- Add new products with name, category, price, and stock quantity
- Edit existing products and update stock levels
- View all products with stock status indicators
- Automatic low-stock alerts for items under 5 units

### Sales Recording
- Select products from inventory
- Automatic price calculation based on quantity
- Real-time stock validation and updates
- Sales history with comprehensive tracking

### Repair Services
- Add repair jobs with customer information
- Track device details and issue descriptions
- Manage repair status (Pending, In Progress, Completed, Delivered)
- Cost tracking for repair services

### Dashboard
- Live view of today's sales total
- Low-stock product alerts
- Pending repairs counter
- Recent sales overview
- Quick action buttons for common tasks

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **Icons**: Bootstrap Icons

## Project Structure

```
├── app.py                 # Main Flask application
├── models.py             # Database models
├── requirements.txt      # Python dependencies
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── dashboard.html   # Main dashboard
│   ├── products.html    # Product management
│   ├── sales.html       # Sales history
│   └── repairs.html     # Repair management
└── static/             # Static assets
    ├── css/style.css   # Custom styling
    └── js/main.js      # JavaScript functionality
```

## Design

The system follows a clean, modern design inspired by Square POS and Shopify's admin interface:

- **Colors**: Primary green (#28A745), secondary blue (#007BFF), warning yellow (#FFC107)
- **Typography**: Inter/Roboto font family
- **Layout**: Card-based design with responsive grid
- **User Experience**: Intuitive navigation with clear visual feedback

## License

This project is created for educational purposes.