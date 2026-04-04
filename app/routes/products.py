from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from peewee import IntegrityError
from app.models.product import Product

products_bp = Blueprint("products", __name__)

@products_bp.route("/products", methods=["GET"])
def list_products():
    products = Product.select()
    return jsonify([model_to_dict(p) for p in products])

@products_bp.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Bad Input: 'name' and 'price' are required"}), 400
    try:
        p = Product.create(
            name=data['name'], 
            category=data.get('category', 'General'), 
            price=data['price'], 
            stock=data.get('stock', 0)
        )
        return jsonify(model_to_dict(p)), 201
    except IntegrityError:
        return jsonify({"error": "Data constraint error (Duplicate or negative value)"}), 409
    except Exception:
        return jsonify({"error": "Internal server error"}), 500

@products_bp.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    try:
        p = Product.get_by_id(product_id)
        return jsonify(model_to_dict(p))
    except Product.DoesNotExist:
        return jsonify({"error": "Product not found"}), 404
