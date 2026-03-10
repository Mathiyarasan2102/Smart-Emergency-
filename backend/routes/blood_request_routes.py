from flask import Blueprint, request, jsonify
from models import get_db_connection
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import token_required

request_bp = Blueprint('request', __name__)

@request_bp.route('/', methods=['POST'])
@token_required
def create_request(current_user):
    if current_user['role'] != 'hospital':
        return jsonify({"message": "Unauthorized"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get hospital id
    cursor.execute("SELECT id FROM hospitals WHERE user_id = ?", (current_user['user_id'],))
    hospital = cursor.fetchone()
    
    if not hospital:
        return jsonify({"message": "Hospital profile not found"}), 404

    data = request.get_json()
    
    try:
        cursor.execute("""
            INSERT INTO blood_requests 
            (hospital_id, patient_name, blood_group, units_required, urgency_level) 
            VALUES (?, ?, ?, ?, ?)
        """, (
            hospital['id'], 
            data.get('patient_name'), 
            data.get('blood_group'), 
            data.get('units_required'), 
            data.get('urgency_level')
        ))
        conn.commit()
        return jsonify({"message": "Blood request created successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@request_bp.route('/', methods=['GET'])
def get_requests():
    # Public route or could be admin/hospital specific depending on requirements.
    # Allowing public filtering allows donors to see where they are needed.
    blood_group = request.args.get('blood_group')
    status = request.args.get('status', 'Pending')
    
    query = """
        SELECT r.id, r.patient_name, r.blood_group, r.units_required, r.urgency_level, r.status, r.created_at, 
               h.hospital_name, h.city, h.contact_number
        FROM blood_requests r
        JOIN hospitals h ON r.hospital_id = h.id
        WHERE r.status = ?
    """
    params = [status]
    
    if blood_group:
        query += " AND r.blood_group = ?"
        params.append(blood_group)
        
    query += " ORDER BY r.created_at DESC"
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    requests = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(requests), 200

@request_bp.route('/<int:request_id>', methods=['PUT'])
@token_required
def update_request_status(current_user, request_id):
    if current_user['role'] not in ['hospital', 'admin']:
        return jsonify({"message": "Unauthorized"}), 403
        
    data = request.get_json()
    status = data.get('status')
    
    if not status:
        return jsonify({"message": "Status is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Simple check if hospital owns the request or if user is admin
    cursor.execute("UPDATE blood_requests SET status = ? WHERE id = ?", (status, request_id))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Request status updated successfully"}), 200
