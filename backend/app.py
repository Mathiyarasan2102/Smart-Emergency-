import sqlite3
import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from werkzeug.security import generate_password_hash

# Import routes
from routes.auth_routes import auth_bp
from routes.donor_routes import donor_bp
from routes.hospital_routes import hospital_bp
from routes.admin_routes import admin_bp
from routes.blood_request_routes import request_bp

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for all routes (important for separate frontend)
CORS(app)

# Register Blueprints for modularity
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(donor_bp, url_prefix='/api/donors')
app.register_blueprint(hospital_bp, url_prefix='/api/hospitals')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(request_bp, url_prefix='/api/requests')

def init_db():
    schema_path = os.path.join(Config.BASE_DIR, 'database', 'schema.sql')
    db_path = Config.DATABASE_URI
    
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))

    with app.app_context():
        conn = sqlite3.connect(db_path)
        with open(schema_path, mode='r') as f:
            conn.cursor().executescript(f.read())
        
        # Insert default admin if not exists
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username='admin'")
        if not cursor.fetchone():
            hashed_password = generate_password_hash('admin123')
            cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                           ('admin', hashed_password, 'admin'))
        
        # Insert initial dummy inventory if empty
        cursor.execute("SELECT COUNT(*) FROM blood_inventory")
        if cursor.fetchone()[0] == 0:
            blood_groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
            for bg in blood_groups:
                cursor.execute("INSERT INTO blood_inventory (blood_group, units_available) VALUES (?, 0)", (bg,))

        conn.commit()
        conn.close()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Smart Emergency Blood & Donor Management API"})

if __name__ == '__main__':
    # Initialize DB before running
    if not os.path.exists(Config.DATABASE_URI):
        print("Initializing database...")
        init_db()
        print("Database created and seeded.")
    app.run(debug=True, port=5000, use_reloader=False)
