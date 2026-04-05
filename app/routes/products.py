from flask import Blueprint, jsonify, request, redirect
from app.models.product import Url
import string
import random
from datetime import datetime

products_bp = Blueprint("products", __name__)

@products_bp.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    if not data or 'original_url' not in data:
        return jsonify({"error": "original_url is required"}), 400
    
    short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    
    try:
        Url.create(
            user_id=1, 
            short_code=short_code,
            original_url=data['original_url'],
            title=data.get('title', 'Manual Shortened URL'),
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        return jsonify({"short_code": short_code, "original_url": data['original_url']}), 201
    except Exception as e:
        return jsonify({"error": "Failed to save URL", "details": str(e)}), 500

@products_bp.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    try:
        url_entry = Url.get(Url.short_code == short_code)
        
        if not url_entry.is_active:
            return jsonify({"error": "This URL has been deactivated"}), 403
            
        return redirect(url_entry.original_url)
    except Url.DoesNotExist:
        return jsonify({"error": "URL not found"}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500