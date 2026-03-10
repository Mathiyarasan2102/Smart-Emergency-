from flask import Blueprint, jsonify
from models import get_db_connection
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import token_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/stats', methods=['GET'])
@token_required
def get_stats(current_user):
    if current_user['role'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM donors")
    total_donors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM hospitals")
    total_hospitals = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM blood_requests")
    total_requests = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "donors": total_donors,
        "hospitals": total_hospitals,
        "requests": total_requests
    }), 200

@admin_bp.route('/users', methods=['GET'])
@token_required
def get_all_users(current_user):
    if current_user['role'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role FROM users")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify(users), 200
