from flask import Blueprint, jsonify
from models import get_db_connection
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import token_required

hospital_bp = Blueprint('hospital', __name__)

@hospital_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    if current_user['role'] != 'hospital':
        return jsonify({"message": "Unauthorized"}), 403
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hospitals WHERE user_id = ?", (current_user['user_id'],))
    hospital = cursor.fetchone()
    conn.close()
    
    if hospital:
        return jsonify(dict(hospital)), 200
    return jsonify({"message": "Hospital not found"}), 404
