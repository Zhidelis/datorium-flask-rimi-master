import os
from peewee import SqliteDatabase
from flask import Flask, render_template


def register_blueprints(app):
    from blueprints.auth.views import auth_bp
    from blueprints.admin.views import admin_bp
    from blueprints.product.views import product_bp
    from blueprints.cart.views import cart_bp
    from blueprints.user.views import user_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(user_bp)


db = SqliteDatabase('eshop.db')
app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)


# Automatically creates a Uploads dir
# on Flask start
upload_folder_name = 'uploads'
project_root_dir = os.path.dirname(__file__)
upload_dir = os.path.join(project_root_dir, upload_folder_name)
if not os.path.exists(upload_dir):
    os.mkdir(upload_dir)


app.config['SECRET_KEY'] = 'ssshhh'
app.config['UPLOAD_FOLDER'] = upload_dir
app.config['VALID_IMAGE_FORMATS'] = ['png', 'jpg', 'jpeg']


@app.route('/')
def home():
    from blueprints.product.models import Product
    products = Product.get_available_products()
    return render_template('home.html', products=products)


if __name__ == '__main__':
    register_blueprints(app)
    app.run(debug=True)
