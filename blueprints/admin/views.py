import datetime as dt
from app import app
from flask import (
    Blueprint,
    render_template,
    abort,
    request,
    session,
    redirect,
    url_for,
    flash
)

from blueprints.admin.utils import upload_image
from blueprints.auth.models import User
from blueprints.admin.forms import AdminProductForm, AdminProductEditForm
from blueprints.product.models import Product, ProductImage


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/users')
def users_overview():
    current_user_id = session.get('user_id')
    users = User.select().where(User.id != current_user_id)
    return render_template('admin/users/overview.html', users=users)


@admin_bp.route('/users/<int:user_id>')
def users_view(user_id):
    try:
        user = User.get_by_id(user_id)
        return render_template('admin/users/view.html', user=user)
    except User.DoesNotExist:
        abort(404)


@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def users_edit(user_id):
    try:
        user = User.get_by_id(user_id)
    except User.DoesNotExist:
        abort(404)

    if request.method == 'POST':
        user.name = request.form.get('name')
        user.email = request.form.get('email')
        user.is_admin = request.form.get('is_admin')
        user.updated_at = dt.datetime.now()
        user.save()

    return render_template('admin/users/edit.html', user=user)


@admin_bp.route('/users/<int:user_id>/delete')
def users_delete(user_id):
    if int(user_id) == int(session.get('user_id')):
        abort(403)

    try:
        user = User.get_by_id(user_id)
        user.delete_instance()
        return redirect(url_for('admin.users_overview'))
    except User.DoesNotExist:
        abort(404)


# Products functions
# products_overview
# products_view
# products_add
# products_edit
# products_delete


@admin_bp.route('/products')
def products_overview():
    products = Product.select()
    return render_template('admin/products/overview.html', products=products)


@admin_bp.route('/products/add', methods=['GET', 'POST'])
def products_add():
    form = AdminProductForm()
    if form.validate_on_submit():
        product = Product.create(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            stock=form.stock.data,
            hidden=form.hidden.data
        )

        if form.image.data:
            img_path, img_name = upload_image(app.config['UPLOAD_FOLDER'], form.image.data)
            ProductImage.create(
                image=img_name,
                product=product
            )

        msg = f'Product {product.name} successfully added!'
        flash(msg, 'success')
        return redirect(url_for('admin.products_overview'))

    return render_template('admin/products/add.html', form=form)


@admin_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
def products_edit(product_id):
    try:
        product = Product.get_by_id(product_id)
    except Product.DoesNotExist:
        abort(404)

    form = AdminProductEditForm()
    if form.validate_on_submit():
        if form.image.data:
            # output = (image_path, image_name)
            # output[0]
            # img_path, img_name = upload_image(...)
            img_path, img_name = upload_image(app.config['UPLOAD_FOLDER'], form.image.data)

            # Create record in database if
            # image successfully uploaded
            ProductImage.create(
                image=img_name,
                product=product
            )

        product.name = form.name.data
        product.price = form.price.data
        product.description = form.description.data
        product.stock = form.stock.data
        product.hidden = form.hidden.data
        product.save()

    return render_template('admin/products/edit.html', form=form, product=product)


@admin_bp.route('/products/<int:product_id>/delete')
def products_delete(product_id):
    try:
        product = Product.get_by_id(product_id)
        product.delete_instance()
        msg = f'Product {product.name} deleted successfully'
        flash(msg, 'success')
        return redirect(url_for('admin.products_overview'))
    except Product.DoesNotExist:
        abort(404)
