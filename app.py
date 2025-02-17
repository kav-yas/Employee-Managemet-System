from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# Flask App Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///signifyflask.db'
app.config['SECRET_KEY'] = 'secretkey'

# Database & Security Setup
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Employee Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 🔹 Home Route
@app.route("/")
def home():
    return render_template("home.html")

# 🔹 Register Route
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username_html = request.form['username']
        password_html = request.form['password']
        
        # Check if user already exists
        existing_user = User.query.filter_by(username=username_html).first()
        if existing_user:
            return "User already exists, try a different username."
        
        # Hash password and add user
        hash_password = bcrypt.generate_password_hash(password_html).decode('utf-8')
        user = User(username=username_html, password=hash_password)
        
        db.session.add(user)
        db.session.commit()  # ✅ Ensure changes are saved
        
        return redirect(url_for('login'))
    return render_template("register.html")


# 🔹 Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Add authentication logic here
        return redirect(url_for('home'))
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

# 🔹 Logout Route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

# 🔹 Employee Dashboard
@app.route("/employee_dashboard")
@login_required
def employee_dashboard():
    return render_template("employee_dashboard.html")

# 🔹 Admin Dashboard
@app.route("/admin_dashboard")
@login_required
def admin_dashboard():
    return render_template("admin_dashboard.html")

# 🔹 Leave Management
@app.route("/leave_management")
@login_required
def leave_management():
    return render_template("leave_management.html")

# 🔹 Payroll & Performance
@app.route("/payroll_performance")
@login_required
def payroll_performance():
    return render_template("payroll_performance.html")

# Database Creation
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
