from flask import jsonify, request


from app import db
from app.chemas import ProductSchema
from app.models import Product
from app.utils import ModelTransfer
from . import product

model_transfer = ModelTransfer(ProductSchema)


@product.route("/admin/product/all")
def get_all_products():
    products = Product.query.all()
    return model_transfer.to_response(products)


@product.route("/admin/product/newest")
def get_newest_products():
    products = Product.query.filter(Product.isNewest).all()
    return jsonify(products), 200


@product.route("/admin/product")
def get_product_by_id():
    productId = request.args.get('productId')
    product = Product.query.filter(Product.id == productId).first()
    return model_transfer.to_response(product)




@product.route("/admin/product", methods=['PUT', 'POST', 'DELETE'])
def create_product():
    if request.method == 'DELETE':
        _delete_product(request.args.get("productId"))
    else:
        data = request.get_json()
        if request.method == 'POST':
            _add_product(data)
        else:
            _update_product(data)
    db.session.commit()
    return "OK", 200


def _delete_product(product_id):
    data = Product.query.filter(Product.id == product_id).first()
    db.session.delete(data)


def _add_product(data):
    product_new = Product()
    for key in data:
        product_new.__setattr__(key, data[key])
    db.session.add(product_new)


def _update_product(data):
    Product.query.filter(Product.id == data['id']).update(data)
