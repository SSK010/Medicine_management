from flask import Flask, redirect, url_for, render_template, flash, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import bcrypt
from config import DB_PATH, SECRET_KEY
from routes import routes  # Import the Blueprint

app = Flask(__name__)
app.secret_key = SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Ensure unauthenticated users go to login

# User Model
class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1], user[3])
    return None

# Home Route
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
            user_obj = User(user[0], user[1], user[3])
            login_user(user_obj)
            flash("✅ Login successful!", "success")
            return redirect(url_for('dashboard'))
        flash("❌ Invalid username or password.", "error")

    return render_template('login.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("✅ You have been logged out.", "success")
    return redirect(url_for('login'))  # Redirect to login after logout

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Save user to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                           (username, hashed_password.decode('utf-8'), role))
            conn.commit()
            flash("✅ Registration successful! You can now login.", "success")
            return redirect(url_for('login'))
        except sqlite3.Error as e:
            flash(f"❌ Error: {e}", "error")
        finally:
            conn.close()

    return render_template('register.html')

# Dashboard Redirect Based on Role
@app.route('/dashboard')
@login_required
def dashboard():
    role_redirects = {
        "Admin": "routes.admin_dashboard",
        "Doctor": "routes.doctor_dashboard",
        "Nurse": "routes.nurse_dashboard",
        "Guest": "routes.guest_dashboard"
    }
    return redirect(url_for(role_redirects.get(current_user.role, 'routes.dashboard')))

# Register Blueprint
app.register_blueprint(routes, url_prefix='/')  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

