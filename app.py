from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Product, Sale, Repair
from datetime import datetime, date
from sqlalchemy import func
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pos_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# This will be handled in the main section

# Dashboard Route
@app.route('/')
def dashboard():
    # Get today's sales total
    today = date.today()
    today_sales = db.session.query(func.sum(Sale.total_price)).filter(
        func.date(Sale.sale_date) == today
    ).scalar() or 0
    
    # Get low stock products (under 5 items)
    low_stock_products = Product.query.filter(Product.stock < 5).all()
    
    # Get recent sales
    recent_sales = Sale.query.order_by(Sale.sale_date.desc()).limit(5).all()
    
    # Get pending repairs
    pending_repairs = Repair.query.filter_by(status='Pending').count()
    
    return render_template('dashboard.html', 
                         today_sales=today_sales,
                         low_stock_products=low_stock_products,
                         recent_sales=recent_sales,
                         pending_repairs=pending_repairs)

# Product Management Routes
@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        
        new_product = Product(name=name, category=category, price=price, stock=stock)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('add_product.html')

@app.route('/products/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form['name']
        product.category = request.form['category']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    
    return render_template('edit_product.html', product=product)

@app.route('/products/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('products'))

# Sales Routes
@app.route('/sales')
def sales():
    sales = Sale.query.order_by(Sale.sale_date.desc()).all()
    return render_template('sales.html', sales=sales)

@app.route('/sales/add', methods=['GET', 'POST'])
def add_sale():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        quantity = int(request.form['quantity'])
        
        product = Product.query.get_or_404(product_id)
        
        if product.stock < quantity:
            flash('Insufficient stock!', 'error')
            return redirect(url_for('add_sale'))
        
        total_price = product.price * quantity
        
        # Create sale record
        new_sale = Sale(product_id=product_id, quantity=quantity, total_price=total_price)
        db.session.add(new_sale)
        
        # Update product stock
        product.stock -= quantity
        
        db.session.commit()
        flash('Sale recorded successfully!', 'success')
        return redirect(url_for('sales'))
    
    products = Product.query.filter(Product.stock > 0).all()
    return render_template('add_sale.html', products=products)

# Repair Routes
@app.route('/repairs')
def repairs():
    repairs = Repair.query.order_by(Repair.created_at.desc()).all()
    return render_template('repairs.html', repairs=repairs)

@app.route('/repairs/add', methods=['GET', 'POST'])
def add_repair():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_phone = request.form['customer_phone']
        device_type = request.form['device_type']
        device_model = request.form['device_model']
        issue_description = request.form['issue_description']
        repair_cost = float(request.form['repair_cost'])
        
        new_repair = Repair(
            customer_name=customer_name,
            customer_phone=customer_phone,
            device_type=device_type,
            device_model=device_model,
            issue_description=issue_description,
            repair_cost=repair_cost
        )
        
        db.session.add(new_repair)
        db.session.commit()
        flash('Repair job added successfully!', 'success')
        return redirect(url_for('repairs'))
    
    return render_template('add_repair.html')

@app.route('/repairs/edit/<int:id>', methods=['GET', 'POST'])
def edit_repair(id):
    repair = Repair.query.get_or_404(id)
    
    if request.method == 'POST':
        repair.customer_name = request.form['customer_name']
        repair.customer_phone = request.form['customer_phone']
        repair.device_type = request.form['device_type']
        repair.device_model = request.form['device_model']
        repair.issue_description = request.form['issue_description']
        repair.repair_cost = float(request.form['repair_cost'])
        repair.status = request.form['status']
        repair.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Repair job updated successfully!', 'success')
        return redirect(url_for('repairs'))
    
    return render_template('edit_repair.html', repair=repair)

@app.route('/repairs/delete/<int:id>')
def delete_repair(id):
    repair = Repair.query.get_or_404(id)
    db.session.delete(repair)
    db.session.commit()
    flash('Repair job deleted successfully!', 'success')
    return redirect(url_for('repairs'))

# API Routes for AJAX
@app.route('/api/product/<int:id>')
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'stock': product.stock
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)