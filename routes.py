# from flask import Blueprint, render_template, request, redirect, url_for
# from models import db, User

# routes = Blueprint("routes", __name__)

# @routes.route('/')
# def home():
#     return render_template('login.html')

# @routes.route('/login', methods=['POST'])
# def login():
#     email = request.form.get('email')
#     password = request.form.get('password')
#     login_type = request.form.get('login_type')

#     user = User.query.filter_by(email=email).first()

#     if user and user.check_password(password):
#         if login_type == "admin" and user.role == "admin":
#             return redirect(url_for('routes.dashboard'))
#         elif login_type == "user" and user.role == "user":
#             return redirect(url_for('routes.section'))

#     return redirect(url_for('routes.home'))

# @routes.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')

# @routes.route('/section')
# def section():
#     return render_template('section.html')
