# 🩸 Smart Emergency Blood & Donor Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-REST%20API-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Frontend](https://img.shields.io/badge/Frontend-HTML%20%7C%20CSS%20%7C%20JS-orange.svg)]()
[![Database](https://img.shields.io/badge/Database-SQLite-blue.svg)]()

A full-stack web application designed to bridge the gap between blood donors, hospitals, and patients quickly during critical emergencies. This system provides a streamlined platform for real-time blood requests, donor availability tracking, and hospital management.

---

## 🚀 Features
- **Role-Based Access:** Dedicated dashboards for Admins, Hospitals, and Donors.
- **Emergency Blood Requests:** Hospitals can broadcast urgent blood requirements.
- **Real-Time Donor Tracking:** Donors can update their availability status instantly.
- **Global Search:** Public page to find available donors by blood group and city.
- **Secure Authentication:** JWT-based token authentication for all user roles.
- **Automated Setup:** Database auto-initializes upon first run with a default Admin account.

---

## 🛠️ Project Architecture
- **Backend:** Python, Flask (REST API architecture)
- **Database:** SQLite (Relational DB)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)
- **Security:** PyJWT for token-based authentication, Werkzeug for password hashing.

---

## 📋 Prerequisites
Before you begin, ensure you have the following installed on your machine:
- [Python 3.8+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)

---

## ⚙️ Setup & Installation Instructions

### 1. Clone the Repository
```bash
git clone <your-github-repo-url>
cd "Smart Emergency"
```

### 2. Backend Installation & Database Setup
It is recommended to use a virtual environment to manage dependencies.

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required Python packages:
```bash
pip install -r requirements.txt
```

Start the backend server:
```bash
python backend/app.py
```
> **Note:** Running this file for the first time automatically generates the `database/blood_bank.db` file and inserts a default Admin user:
> - **Username:** `admin`
> - **Password:** `admin123`

### 3. Frontend Execution
The frontend uses plain HTML/CSS/Vanilla JS and communicates with the backend via REST API calls. You do not need Node.js to run it.

Choose one of the following methods:

**Method A (Direct File Open):**
Navigate to the `frontend` folder and double-click `index.html` to open it directly in your web browser.

**Method B (Local Python Server - Recommended to avoid CORS issues):**
Open a **new terminal window**, navigate to the `frontend` folder, and start a simple web server:
```bash
cd frontend
python -m http.server 8000
```
Then, open your web browser and navigate to: `http://localhost:8000/index.html`

---

## 🧪 How to Use & Test the System

1. **Admin Dashboard:**
   - Go to the login page and sign in as **admin / admin123**. 
   - View system statistics, total donors, and active requests.

2. **Donor Registration & Activity:**
   - Register a new user as a **Donor**, providing your blood group and city. 
   - Once logged in, use the "Mark Available" status on the Donor Dashboard.

3. **Hospital Registration & Emergency Flow:**
   - Register a new user as a **Hospital**, providing the hospital name and address.
   - Sign in as the Hospital and choose "New Blood Request" to submit an urgent requirement for a specific blood type.
   - The registered Donor will now be able to see these urgent requirements on their dashboard.

4. **Global Search:**
   - Visit the homepage and use the "Find Donors" tab to search for the newly registered donor.

5. **Request Fulfillment:** 
   - Once the hospital connects with a donor, the hospital can mark the request as "Fulfilled" directly from their dashboard.

---

## 📁 Project Structure
```text
Smart Emergency/
├── backend/                  # Flask API source code
│   ├── app.py                # Main application entry point
│   ├── config.py             # Configuration settings
│   ├── models.py             # Database models
│   ├── utils.py              # Helper functions (auth, etc)
│   └── routes/               # API endpoint definitions
├── database/                 # SQLite database storage (auto-generated)
├── frontend/                 # Static HTML, CSS, JS files
│   ├── index.html            # Landing page
│   ├── css/                  # Stylesheets
│   └── js/                   # Vanilla JavaScript modules
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```
