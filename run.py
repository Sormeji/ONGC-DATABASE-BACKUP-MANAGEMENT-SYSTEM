# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from flask_sqlalchemy import SQLAlchemy
# from functools import wraps
# from datetime import datetime
# from flask_migrate import Migrate

# app = Flask(__name__)
# app.secret_key = "your_secret_key"

# # Database Configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/ongc_backup_database'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize Database & Migrations
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# # User Model
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), nullable=False, unique=True)
#     password = db.Column(db.String(50), nullable=False)
#     role = db.Column(db.String(10), nullable=False)  # 'admin' or 'user'

# # Backup Record Model
# class BackupRecord(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     backup_type = db.Column(db.String(50), nullable=False)
#     backup_frequency = db.Column(db.String(20), nullable=False)  # Add this column
#     tape_number = db.Column(db.String(50), nullable=False)
#     backup_date = db.Column(db.Date, nullable=False)
#     server = db.Column(db.String(100), nullable=False)
#     os = db.Column(db.String(50), nullable=False)
#     backup_contents = db.Column(db.Text, nullable=False)
#     backup_format = db.Column(db.String(50), nullable=False)
#     remarks = db.Column(db.Text, nullable=True)
#     tape_reuse_date = db.Column(db.Date, nullable=True)
#     extra_info = db.Column(db.Text, nullable=True)


# # Dummy user database
# users = {
#     "admin": {"username": "admin", "password": "admin123", "role": "admin"},
#     "user": {"username": "user", "password": "user123", "role": "user"}
# }

# # Authentication Decorator
# def login_required(role=None):
#     def decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             if "user" not in session:
#                 flash("You must be logged in to access this page.", "error")
#                 return redirect(url_for('home'))

#             if role and session.get("role") != role:
#                 flash("Unauthorized access!", "error")
#                 return redirect(url_for('home'))

#             return f(*args, **kwargs)
#         return wrapper
#     return decorator

# # Routes
# @app.route('/')
# def home():
#     return render_template('login.html')

# @app.route('/login', methods=['POST'])
# def login():
#     username = request.form.get('username')
#     password = request.form.get('password')
#     role = request.form.get('role')

#     if username in users and users[username]["password"] == password and users[username]["role"] == role:
#         session["user"] = username
#         session["role"] = role
#         session.permanent = True
#         flash(f"Welcome, {username}!", "success")
#         return redirect(url_for('dashboard' if role == "admin" else 'section'))

#     flash("Invalid Credentials. Please try again.", "error")
#     return redirect(url_for('home'))

# @app.route('/dashboard')
# @login_required(role="admin")
# def dashboard():
#     return render_template('dashboard.html', username=session["user"])

# @app.route('/section')
# @login_required(role="user")
# def section():
#     return render_template('section.html', username=session["user"])

# @app.route('/logout')
# def logout():
#     session.pop("user", None)
#     session.pop("role", None)
#     flash("You have been logged out.", "info")
#     return redirect(url_for('home'))

# # Backup Form Submission
# @app.route('/backup_redirect', methods=['POST'])
# @login_required()
# def backup_redirect():
#     try:
#         backup_type = request.form.get('backup_type')
#         backup_frequency = request.form.get('backup_frequency')
#         tape_number = request.form.get('tape_number')
#         backup_date_str = request.form.get('backup_date')
#         server = request.form.get('server')
#         os = request.form.get('os')
#         backup_contents = request.form.get('backup_contents')
#         backup_format = request.form.get('backup_format')
#         remarks = request.form.get('remarks')
#         tape_reuse_date_str = request.form.get('tape_reuse_date')
#         extra_info = request.form.get('extra_info')

#         # Convert date fields safely
#         backup_date = datetime.strptime(backup_date_str, '%Y-%m-%d') if backup_date_str else None
#         tape_reuse_date = datetime.strptime(tape_reuse_date_str, '%Y-%m-%d') if tape_reuse_date_str else None

#         if not all([backup_type, backup_frequency, tape_number, backup_date, server, os, backup_contents, backup_format]):
#             flash("All required fields must be filled!", "error")
#             return redirect(request.referrer)

#         # Create and save new backup record
#         new_backup = BackupRecord(
#             backup_type=backup_type,
#             backup_frequency=backup_frequency,
#             tape_number=tape_number,
#             backup_date=backup_date,
#             server=server,
#             os=os,
#             backup_contents=backup_contents,
#             backup_format=backup_format,
#             remarks=remarks,
#             tape_reuse_date=tape_reuse_date,
#             extra_info=extra_info
#         )

#         db.session.add(new_backup)
#         db.session.commit()
#         flash("Backup record successfully added!", "success")

#         # Redirect to the respective page with the correct frequency
#         if backup_type == "nas":
#             return redirect(url_for('nas_backup', frequency=backup_frequency))
#         elif backup_type == "room_no_1":
#             return redirect(url_for('room_no_1', frequency=backup_frequency))
#         elif backup_type == "logging_section":
#             return redirect(url_for('logging_section', frequency=backup_frequency))
#         elif backup_type == "corporate_eds":
#             return redirect(url_for('corporate_eds', frequency=backup_frequency))

#     except Exception as e:
#         db.session.rollback()
#         flash(f"Database error occurred: {str(e)}", "error")

#     return redirect(request.referrer)


# # Routes for Different Backup Sections
# @app.route('/nas_backup', methods=['GET'])
# @login_required()
# def nas_backup():
#     frequency = request.args.get('frequency', 'daily')  # Default to 'daily'
#     records = BackupRecord.query.filter_by(backup_type="nas", backup_frequency=frequency).all()
#     return render_template('nas_backup.html', records=records, frequency=frequency)

# @app.route('/room_no_1')
# @login_required()
# def room_no_1():
#     frequency = request.args.get('frequency', 'daily')
#     records = BackupRecord.query.filter_by(backup_type="room_no_1", backup_frequency=frequency).all()
#     return render_template('room_no_1.html', records=records, frequency=frequency)

# @app.route('/logging_section')
# @login_required()
# def logging_section():
#     frequency = request.args.get('frequency', 'daily')
#     records = BackupRecord.query.filter_by(backup_type="logging_section", backup_frequency=frequency).all()
#     return render_template('logging_section.html', records=records, frequency=frequency)

# @app.route('/corporate_eds')
# @login_required()
# def corporate_eds():
#     frequency = request.args.get('frequency', 'daily')
#     records = BackupRecord.query.filter_by(backup_type="corporate_eds", backup_frequency=frequency).all()
#     return render_template('corporate_eds.html', records=records, frequency=frequency)


# # Test Database Connection
# @app.route('/test_db')
# @login_required(role="admin")
# def test_db():
#     try:
#         records = BackupRecord.query.all()  # Attempt to retrieve all records
#         return f"Database connection successful! Number of records: {len(records)}"
#     except Exception as e:
#         return f"Database connection failed: {str(e)}"

# # Backup Forms

# @app.route('/daily_backup', methods=['GET', 'POST'])
# @login_required()
# def add_daily_backup():
#     if request.method == 'POST':
#         flash("Daily backup submitted successfully!", "success")
#         return redirect(url_for('dashboard'))
#     return render_template('daily_backup_form.html')

# @app.route('/monthly_backup', methods=['GET', 'POST'])
# @login_required()
# def add_monthly_backup():
#     if request.method == 'POST':
#         flash("Monthly backup submitted successfully!", "success")
#         return redirect(url_for('dashboard'))
#     return render_template('monthly_backup_form.html')

# @app.route('/yearly_backup', methods=['GET', 'POST'])
# @login_required()
# def add_yearly_backup():
#     if request.method == 'POST':
#         flash("Yearly backup submitted successfully!", "success")
#         return redirect(url_for('dashboard'))
#     return render_template('yearly_backup_form.html')

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
