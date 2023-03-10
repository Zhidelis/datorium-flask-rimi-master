import datetime as dt
from app import app
from flask import Blueprint, send_from_directory, session, url_for, redirect
from blueprints.product.models import Product, ProductImage
from blueprints.cart.models import Cart, CartItem


product_bp = Blueprint('product', __name__, url_prefix='/products')
Product.create_table()
ProductImage.create_table()


@product_bp.route('/uploads/<string:filename>')
def product_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@product_bp.route('/<int:product_id>/add-to-cart')
def add_to_cart(product_id):
    user_id = session.get('user_id')
    product = Product.get_by_id(product_id)
    cart = Cart.get_active_cart(user_id)

    cart_items = CartItem.filter(cart=cart, product=product)
    if not cart_items:
        CartItem.create(
            cart=cart,
            product=product
        )
    else:
        cart_item = cart_items[0]
        cart_item.amount += 1
        cart_item.updated_at = dt.datetime.now()
        cart_item.save()

    return redirect(url_for('home'))
