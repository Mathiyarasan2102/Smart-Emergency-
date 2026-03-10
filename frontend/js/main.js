// Base URL for API
const API_URL = 'http://localhost:5000/api';

// Authentication Management
function setSession(token, role) {
    localStorage.setItem('token', token);
    localStorage.setItem('role', role);
}

function getToken() {
    return localStorage.getItem('token');
}

function getRole() {
    return localStorage.getItem('role');
}

function clearSession() {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    window.location.href = 'index.html';
}

function getAuthHeaders() {
    const token = getToken();
    return {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
    };
}

// Check access controls
function requireRole(allowedRoles) {
    const currentRole = getRole();
    if (!currentRole || !allowedRoles.includes(currentRole)) {
        alert("Unauthorized access. Redirecting to login...");
        window.location.href = 'login.html';
    }
}

// Display Alerts
function showAlert(message, type = 'error') {
    const alertBox = document.getElementById('alert-box');
    if (!alertBox) return;
    
    alertBox.textContent = message;
    alertBox.className = `alert alert-${type}`;
    alertBox.style.display = 'block';
    
    setTimeout(() => {
        alertBox.style.display = 'none';
        alertBox.className = 'alert';
    }, 5000);
}

// Common DOM Elements setup after load
document.addEventListener('DOMContentLoaded', () => {
    // Dynamic Navbar based on Auth State
    const role = getRole();
    const navLinks = document.getElementById('nav-links');
    
    if (navLinks) {
        if (role === 'donor') {
            navLinks.innerHTML = `
                <a href="donor-dashboard.html">Dashboard</a>
                <a href="search-donor.html">Find Donors</a>
                <a href="#" onclick="clearSession()" class="btn btn-outline" style="color:var(--primary-red)">Logout</a>
            `;
        } else if (role === 'hospital') {
            navLinks.innerHTML = `
                <a href="hospital-dashboard.html">Dashboard</a>
                <a href="request-blood.html">Request Blood</a>
                <a href="search-donor.html">Find Donors</a>
                <a href="#" onclick="clearSession()" class="btn btn-outline" style="color:var(--primary-red)">Logout</a>
            `;
        } else if (role === 'admin') {
            navLinks.innerHTML = `
                <a href="admin-dashboard.html">Admin Dashboard</a>
                <a href="#" onclick="clearSession()" class="btn btn-outline" style="color:var(--primary-red)">Logout</a>
            `;
        } else {
            // Unauthenticated User
            navLinks.innerHTML = `
                <a href="index.html">Home</a>
                <a href="search-donor.html">Find Donors</a>
                <a href="login.html">Login</a>
                <a href="register.html" class="btn btn-primary">Register</a>
            `;
        }
    }
});
