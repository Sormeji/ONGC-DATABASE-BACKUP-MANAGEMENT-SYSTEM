# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from flask_sqlalchemy import SQLAlchemy
# from functools import wraps
# from datetime import datetime

# app = Flask(__name__)
# app.secret_key = "your_secret_key"

# # Database Configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/ongc_backup_database'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize Database
# db = SQLAlchemy(app)

# # Ensure database tables are created
# with app.app_context():
#     db.create_all()

# # Dummy user database
# users = {
#     "admin": {"username": "admin", "password": "admin123", "role": "admin"},
#     "user": {"username": "user", "password": "user123", "role": "user"}
# }

# # Decorator to protect routes
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

# # Database Model
# class BackupRecord(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     backup_type = db.Column(db.String(50), nullable=False)
#     tape_number = db.Column(db.String(50), nullable=False)
#     backup_date = db.Column(db.Date, nullable=False)
#     server = db.Column(db.String(100), nullable=False)
#     os = db.Column(db.String(50), nullable=False)
#     backup_contents = db.Column(db.Text, nullable=False)
#     backup_format = db.Column(db.String(50), nullable=False)
#     backup_media = db.Column(db.String(50), nullable=False)
#     remarks = db.Column(db.Text, nullable=True)
#     tape_reuse_date = db.Column(db.Date, nullable=True)
#     extra_info = db.Column(db.Text, nullable=True)

#     def __init__(self, backup_type, tape_number, backup_date, server, os, backup_contents,
#                  backup_format, backup_media,  remarks, tape_reuse_date, extra_info):
#         self.backup_type = backup_type
#         self.tape_number = tape_number
#         self.backup_date = backup_date
#         self.server = server
#         self.os = os
#         self.backup_contents = backup_contents
#         self.backup_format = backup_format
#         self.backup_media = backup_media
#         self.remarks = remarks
#         self.tape_reuse_date = tape_reuse_date
#         self.extra_info = extra_info

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
#         session.permanent = True  # Ensure session persists
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

# # Backup Form Submission - Store in Database and Redirect
# @app.route('/backup_redirect', methods=['POST'])
# @login_required()
# def backup_redirect():
#     try:
#         # Extract form data
#         backup_type = request.form.get('backup_type')
#         tape_number = request.form.get('tape_number')
#         backup_date_str = request.form.get('backup_date')
#         server = request.form.get('server')
#         os = request.form.get('os')
#         backup_contents = request.form.get('backup_contents')
#         backup_format = request.form.get('backup_format')
#         backup_media = request.form.get('backup_media') 
#         remarks = request.form.get('remarks')
#         tape_reuse_date_str = request.form.get('tape_reuse_date')
#         extra_info = request.form.get('extra_info')

#         print("Received Form Data:")
#         print(f"Backup Type: {backup_type}")
#         print(f"Tape Number: {tape_number}")
#         print(f"Backup Date: {backup_date_str}")
#         print(f"Server: {server}")
#         print(f"OS: {os}")
#         print(f"Backup Contents: {backup_contents}")
#         print(f"Backup Format: {backup_format}")
#         print(f"Backup Media: {backup_media}")
#         print(f"Remarks: {remarks}")
#         print(f"Tape Reuse Date: {tape_reuse_date_str}")
#         print(f"Extra Info: {extra_info}")

#         # Convert date fields
#         backup_date = datetime.strptime(backup_date_str, '%Y-%m-%d') if backup_date_str else None
#         tape_reuse_date = datetime.strptime(tape_reuse_date_str, '%Y-%m-%d') if tape_reuse_date_str else None

#         # Ensure required fields are present
#         if not all([backup_type, tape_number, backup_date, server, os, backup_contents, backup_format, backup_media]):
#             flash("All required fields must be filled!", "error")
#             return redirect(url_for('dashboard'))

#         # Create a new backup record
#         new_backup = BackupRecord(
#             backup_type=backup_type,
#             tape_number=tape_number,
#             backup_date=backup_date,
#             server=server,
#             os=os,
#             backup_contents=backup_contents,
#             backup_format=backup_format,
#             backup_media=backup_media,
#             remarks=remarks,
#             tape_reuse_date=tape_reuse_date,
#             extra_info=extra_info
#         )

#         db.session.add(new_backup)
#         db.session.commit()
#         flash("Backup record successfully added!", "success")

#         # Redirect based on backup type
#         routes = {
#             "nas": "nas_backup",
#             "room_no_1": "room_no_1",
#             "logging_section": "logging_section",
#             "corporate_eds": "corporate_eds"
#         }

#         # Debugging: Check the selected backup_type before redirecting
#         print(f"Redirecting to: {routes.get(backup_type, 'dashboard')}")

#         # Redirect to the correct page
#         return redirect(url_for(routes.get(backup_type, 'dashboard')))

#     except Exception as e:
#         db.session.rollback()
#         print(f"Database Error: {str(e)}")
#         flash(f"Error: {str(e)}", "error")
#         return redirect(url_for('dashboard'))





# # Routes for Different Backup Sections
# @app.route('/nas_backup')
# @login_required()
# def nas_backup():
#     daily_records = BackupRecord.query.filter_by(backup_type="daily", backup_media="nas").all()
#     monthly_records = BackupRecord.query.filter_by(backup_type="monthly", backup_media="nas").all()
#     yearly_records = BackupRecord.query.filter_by(backup_type="yearly", backup_media="nas").all()

#     return render_template(
#         'nas_backup.html',
#         daily_records=daily_records,
#         monthly_records=monthly_records,
#         yearly_records=yearly_records
#     )





# @app.route('/room_no_1')
# @login_required()
# def room_no_1():
#     daily_records = BackupRecord.query.filter_by(backup_type="daily", backup_media="room_no_1").all()
#     monthly_records = BackupRecord.query.filter_by(backup_type="monthly", backup_media="room_no_1").all()
#     yearly_records = BackupRecord.query.filter_by(backup_type="yearly", backup_media="room_no_1").all()

#     return render_template(
#         'room_no_1.html',
#         daily_records=daily_records,
#         monthly_records=monthly_records,
#         yearly_records=yearly_records
#     )






# @app.route('/logging_section')
# @login_required()
# def logging_section():
#     daily_records = BackupRecord.query.filter_by(backup_type="daily", backup_media="logging_section").all()
#     monthly_records = BackupRecord.query.filter_by(backup_type="monthly", backup_media="logging_section").all()
#     yearly_records = BackupRecord.query.filter_by(backup_type="yearly", backup_media="logging_section").all()

#     return render_template(
#         'logging_section.html',
#         daily_records=daily_records,
#         monthly_records=monthly_records,
#         yearly_records=yearly_records
#     )




# @app.route('/corporate_eds')
# @login_required()
# def corporate_eds():
#     daily_records = BackupRecord.query.filter_by(backup_type="daily", backup_media="corporate_eds").all()
#     monthly_records = BackupRecord.query.filter_by(backup_type="monthly", backup_media="corporate_eds").all()
#     yearly_records = BackupRecord.query.filter_by(backup_type="yearly", backup_media="corporate_eds").all()

#     return render_template(
#         'corporate_eds.html',
#         daily_records=daily_records,
#         monthly_records=monthly_records,
#         yearly_records=yearly_records
#     )





# @app.route('/daily_backup', methods=['GET', 'POST'])
# @login_required()  # Ensures only logged-in users can access this
# def add_daily_backup():
#     if request.method == 'POST':
#         # Process daily backup data
#         flash("Daily backup submitted successfully!", "success")
#         return redirect(url_for('dashboard'))
#     return render_template('daily_backup_form.html')

# @app.route('/monthly_backup', methods=['GET', 'POST'])
# @login_required()  # Protects monthly backup
# def add_monthly_backup():
#     if request.method == 'POST':
#         # Process monthly backup data
#         flash("Monthly backup submitted successfully!", "success")
#         return redirect(url_for('dashboard'))
#     return render_template('monthly_backup_form.html')

# @app.route('/yearly_backup', methods=['GET', 'POST'])
# @login_required()  # Protects yearly backup
# def add_yearly_backup():
#     if request.method == 'POST':
#         # Process yearly backup data
#         flash("Yearly backup submitted successfully!", "success")
#         return redirect(url_for('dashboard'))
#     return render_template('yearly_backup_form.html')


# # Run the App
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)
