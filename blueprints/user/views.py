from flask import Blueprint, render_template
from blueprints.cart.models import Cart, CartItem, Order
from blueprints.cart.forms import CartItemEditForm


user_bp = Blueprint('user', __name__, url_prefix='/users')


@user_bp.route('/<int:user_id>/cart', methods=['GET', 'POST'])
def cart(user_id):
    form = CartItemEditForm()
    _cart = Cart.get_active_cart(user_id)
    cart_items = CartItem.filter(cart=_cart)
    return render_template('users/cart.html', cart=_cart, cart_items=cart_items, form=form)


@user_bp.route('/<int:user_id>/orders')
def orders(user_id):
    carts = Cart.filter(user_id=user_id, active=False)
    _orders = []
    for _cart in carts:
        order = Order.get(Order.cart == _cart)
        _orders.append(order)
    return render_template('users/orders.html', orders=_orders)


@user_bp.route('/<int:user_id>/orders/<int:order_id>')
def order_details(user_id, order_id):
    order = Order.get_by_id(order_id)
    cart_items = CartItem.filter(cart=order.cart)
    return render_template('users/order_details.html', order=order, cart_items=cart_items)
