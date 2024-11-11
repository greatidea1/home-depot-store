from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

# Initialize the Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.secret_key = 'your-secret-key'  # For flashing messages

# Initialize the database
db = SQLAlchemy(app)

# Define the models
class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.args.get('search_query', '')
    products = []

    if search_query:
        # Perform the search
        products = Product.query.filter(Product.product_name.like(f'%{search_query}%')).all()
    elif not search_query:
        # If no search query, show all products
        products = Product.query.all()

    return render_template('index.html', products=products, search_query=search_query)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Extract form data
        product_name = request.form['product_name']
        category_id = request.form['category_id']
        price = request.form['price']
        stock_quantity = request.form['stock_quantity']
        description = request.form['description']

        # Create and add new product to the database
        new_product = Product(
            product_name=product_name,
            category_id=category_id,
            price=price,
            stock_quantity=stock_quantity,
            description=description
        )
        db.session.add(new_product)
        db.session.commit()

        flash('Product added successfully!', 'success')
        return redirect(url_for('index'))

    # Fetch categories for the form dropdown
    categories = Category.query.all()
    return render_template('add_product.html', categories=categories)

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
