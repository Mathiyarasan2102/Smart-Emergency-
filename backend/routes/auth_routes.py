from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from models import get_db_connection
from config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')

    if not username or not password or not role:
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return jsonify({"error": "Username already exists"}), 409

        hashed_pw = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                       (username, hashed_pw, role))
        user_id = cursor.lastrowid
        
        if role == 'donor':
            cursor.execute("""
                INSERT INTO donors (user_id, full_name, blood_group, city, contact_number) 
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, data.get('full_name'), data.get('blood_group'), data.get('city'), data.get('contact_number')))
        elif role == 'hospital':
            cursor.execute("""
                INSERT INTO hospitals (user_id, hospital_name, city, contact_number, address) 
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, data.get('hospital_name'), data.get('city'), data.get('contact_number'), data.get('address')))
        
        conn.commit()
        return jsonify({"message": f"{role.capitalize()} registered successfully!"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        token = jwt.encode({
            'user_id': user['id'],
            'role': user['role'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, Config.SECRET_KEY, algorithm="HS256")
        
        return jsonify({"token": token, "role": user['role'], "message": "Login successful!"}), 200

    return jsonify({"error": "Invalid username or password"}), 401
