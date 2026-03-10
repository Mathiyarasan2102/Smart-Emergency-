from flask import Blueprint, request, jsonify
from models import get_db_connection
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import token_required

donor_bp = Blueprint('donor', __name__)

@donor_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    if current_user['role'] != 'donor':
        return jsonify({"message": "Unauthorized"}), 403
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM donors WHERE user_id = ?", (current_user['user_id'],))
    donor = cursor.fetchone()
    conn.close()
    
    if donor:
        return jsonify(dict(donor)), 200
    return jsonify({"message": "Donor not found"}), 404

@donor_bp.route('/availability', methods=['PUT'])
@token_required
def update_availability(current_user):
    if current_user['role'] != 'donor':
        return jsonify({"message": "Unauthorized"}), 403
        
    data = request.get_json()
    status = data.get('availability_status')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE donors SET availability_status = ? WHERE user_id = ?", 
                   (status, current_user['user_id']))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Availability updated successfully"}), 200

@donor_bp.route('/all', methods=['GET'])
def get_all_active_donors():
    blood_group = request.args.get('blood_group')
    city = request.args.get('city')
    
    query = "SELECT id, full_name, blood_group, city, contact_number, availability_status FROM donors WHERE availability_status = 1"
    params = []
    
    if blood_group:
        query += " AND blood_group = ?"
        params.append(blood_group)
    if city:
        query += " AND city LIKE ?"
        params.append(f"%{city}%")
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    donors = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(donors), 200
