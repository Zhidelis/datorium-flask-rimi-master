from flask import Blueprint, redirect, url_for, session, flash
from blueprints.cart.models import Cart, CartItem, Order
from blueprints.cart.forms import CartItemEditForm


cart_bp = Blueprint('cart', __name__, url_prefix='/carts')
Cart.create_table()
CartItem.create_table()
Order.create_table()


# edit item amount in user cart
# delete items from user cart


@cart_bp.route('/<int:cart_id>/finish')
def finish(cart_id):
    cart = Cart.get_by_id(cart_id)
    cart.active = False
    cart.save()

    Order.create(
        cart=cart,
        total=cart.get_total_price(),
        address='',
    )

    return redirect(url_for('home'))


@cart_bp.route('/<int:cart_id>/item/<int:item_id>/edit', methods=['POST'])
def edit_item(cart_id, item_id):
    user_id = session.get('user_id')
    item = CartItem.get(id=item_id, cart_id=cart_id)

    form = CartItemEditForm()
    if form.validate_on_submit():
        amount = form.amount.data
        item.amount = amount
        item.save()
        flash(f'Product {item.product.name} was updated', 'success')
        return redirect(url_for('user.cart', user_id=user_id))

    flash(f'Product {item.product.name} was not updated', 'danger')
    return redirect(url_for('user.cart', user_id=user_id))


@cart_bp.route('/<int:cart_id>/item/<int:item_id>/delete')
def delete_item(cart_id, item_id):
    user_id = session.get('user_id')
    item = CartItem.get(id=item_id, cart_id=cart_id)
    item.delete_instance()
    flash(f'Product {item.product.name} was deleted successfully', 'success')
    return redirect(url_for('user.cart', user_id=user_id))
