import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from datetime import date
from werkzeug.utils import secure_filename

# --- Flask Setup ---
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'your_secret_key'  

# --- File Upload Configuration ---
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {
    'zip', 'rar', 'tar', 'gz', '7z', 'txt', 'log', 'pdf',
    'docx', 'xlsx', 'jpg', 'jpeg', 'png', 'gif', 'bmp'
}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Helpers ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Database Setup ---
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- Dummy Users (for Login) ---
users = {
    "admin": {"username": "admin", "password": "admin123", "role": "admin"},
    "user": {"username": "user", "password": "user123", "role": "user"}
}

# --- Models ---
class DailyBackup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    backup_type = db.Column(db.String(50))
    tape_number = db.Column(db.String(100))
    backup_date = db.Column(db.Date)
    server = db.Column(db.String(100))
    os = db.Column(db.String(100))
    backup_contents = db.Column(db.Text)
    backup_file = db.Column(db.String(200))
    backup_format = db.Column(db.String(50))
    backup_media = db.Column(db.String(50))
    remarks = db.Column(db.Text)
    tape_reuse_date = db.Column(db.Date)
    extra_info = db.Column(db.Text)

class MonthlyBackup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    backup_type = db.Column(db.String(50))
    tape_number = db.Column(db.String(100))
    backup_date = db.Column(db.Date)
    server = db.Column(db.String(100))
    os = db.Column(db.String(100))
    backup_contents = db.Column(db.Text)
    backup_file = db.Column(db.String(200))
    backup_format = db.Column(db.String(50))
    backup_media = db.Column(db.String(50))
    remarks = db.Column(db.Text)
    tape_reuse_date = db.Column(db.Date)
    extra_info = db.Column(db.Text)

class YearlyBackup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    backup_type = db.Column(db.String(50))
    tape_number = db.Column(db.String(100))
    backup_date = db.Column(db.Date)
    server = db.Column(db.String(100))
    os = db.Column(db.String(100))
    backup_contents = db.Column(db.Text)
    backup_file = db.Column(db.String(200))
    backup_format = db.Column(db.String(50))
    backup_media = db.Column(db.String(50))
    remarks = db.Column(db.Text)
    tape_reuse_date = db.Column(db.Date)
    extra_info = db.Column(db.Text)

# --- Authentication ---
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')

    user = users.get(username)
    if user and user['password'] == password and user['role'] == role:
        session['user'] = username
        session['role'] = role
        flash("Login successful!", "success")
        return redirect(url_for('dashboard' if role == 'admin' else 'section'))

    flash("Invalid credentials or role mismatch.", "error")
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for('home'))

# --- Dashboard / Section ---
@app.route('/dashboard')
def dashboard():
    if session.get('role') != 'admin':
        flash("Access denied: Admins only!", "error")
        return redirect(url_for('home'))
    return render_template('dashboard.html', username=session.get('user'))

@app.route('/section')
def section():
    if session.get('role') != 'user':
        flash("Access denied: Users only!", "error")
        return redirect(url_for('home'))
    return render_template('section.html', username=session.get('user'))

# --- Backup Forms & Processing ---
@app.route('/daily_backup', methods=['GET', 'POST'])
def add_daily_backup():
    if request.method == 'POST':
        backup_type = request.form['backup_type']
        file = request.files.get('backup_file')
        filename = ''
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        try:
            record = DailyBackup(
                backup_type=backup_type,
                tape_number=request.form['tape_number'],
                backup_date=request.form['backup_date'],
                server=request.form['server'],
                os=request.form['os'],
                backup_contents=request.form['backup_contents'],
                backup_file=filename,
                backup_format=request.form['backup_format'],
                backup_media=request.form['backup_media'],
                remarks=request.form.get('remarks'),
                tape_reuse_date=request.form.get('tape_reuse_date') or None,
                extra_info=request.form.get('extra_info')
            )
            db.session.add(record)
            db.session.commit()
            flash("Daily backup added!", "success")
            return redirect_to_backup(backup_type)
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}", "error")
    return render_template('daily_backup_form.html')

@app.route('/monthly_backup', methods=['GET', 'POST'])
def add_monthly_backup():
    if request.method == 'POST':
        backup_type = request.form['backup_type']
        file = request.files.get('backup_file')
        filename = ''
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        try:
            record = MonthlyBackup(
                backup_type=backup_type,
                tape_number=request.form['tape_number'],
                backup_date=request.form['backup_date'],
                server=request.form['server'],
                os=request.form['os'],
                backup_contents=request.form['backup_contents'],
                backup_file=filename,
                backup_format=request.form['backup_format'],
                backup_media=request.form['backup_media'],
                remarks=request.form.get('remarks'),
                tape_reuse_date=request.form.get('tape_reuse_date') or None,
                extra_info=request.form.get('extra_info')
            )
            db.session.add(record)
            db.session.commit()
            flash("Monthly backup added!", "success")
            return redirect_to_backup(backup_type, prefix='monthly_')
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}", "error")
    return render_template('monthly_backup_form.html')

@app.route('/yearly_backup', methods=['GET', 'POST'])
def add_yearly_backup():
    if request.method == 'POST':
        backup_type = request.form['backup_type']
        file = request.files.get('backup_file')
        filename = ''
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        try:
            record = YearlyBackup(
                backup_type=backup_type,
                tape_number=request.form['tape_number'],
                backup_date=request.form['backup_date'],
                server=request.form['server'],
                os=request.form['os'],
                backup_contents=request.form['backup_contents'],
                backup_file=filename,
                backup_format=request.form['backup_format'],
                backup_media=request.form['backup_media'],
                remarks=request.form.get('remarks'),
                tape_reuse_date=request.form.get('tape_reuse_date') or None,
                extra_info=request.form.get('extra_info')
            )
            db.session.add(record)
            db.session.commit()
            flash("Yearly backup added!", "success")
            return redirect_to_backup(backup_type, prefix='yearly_')
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {e}", "error")
    return render_template('yearly_backup_form.html')
# Monthly
@app.route('/monthly_nas_backup')
def monthly_nas_backup():
    return redirect(url_for('nas_backup'))

@app.route('/monthly_room_no_1')
def monthly_room_no_1():
    return redirect(url_for('room_no_1'))

@app.route('/monthly_logging_section')
def monthly_logging_section():
    return redirect(url_for('logging_section'))

@app.route('/monthly_corporate_eds')
def monthly_corporate_eds():
    return redirect(url_for('corporate_eds'))

# Yearly
@app.route('/yearly_nas_backup')
def yearly_nas_backup():
    return redirect(url_for('nas_backup'))

@app.route('/yearly_room_no_1')
def yearly_room_no_1():
    return redirect(url_for('room_no_1'))

@app.route('/yearly_logging_section')
def yearly_logging_section():
    return redirect(url_for('logging_section'))

@app.route('/yearly_corporate_eds')
def yearly_corporate_eds():
    return redirect(url_for('corporate_eds'))


# --- Backup Redirect Helper ---
def redirect_to_backup(backup_type, prefix=''):
    route_map = {
        'nas': f'{prefix}nas_backup',
        'room_no_1': f'{prefix}room_no_1',
        'logging_section': f'{prefix}logging_section',
        'corporate_eds': f'{prefix}corporate_eds',
    }
    return redirect(url_for(route_map.get(backup_type, 'section')))


# --- Backup Display Pages ---
@app.route('/nas_backup')
def nas_backup():
    daily_records = DailyBackup.query.filter_by(backup_type='nas').all()
    monthly_records = MonthlyBackup.query.filter_by(backup_type='nas').all()
    yearly_records = YearlyBackup.query.filter_by(backup_type='nas').all()
    return render_template('nas_backup.html',
                           daily_records=daily_records,
                           monthly_records=monthly_records,
                           yearly_records=yearly_records)

@app.route('/room_no_1')
def room_no_1():
    daily_records = DailyBackup.query.filter_by(backup_type='room_no_1').all()
    monthly_records = MonthlyBackup.query.filter_by(backup_type='room_no_1').all()
    yearly_records = YearlyBackup.query.filter_by(backup_type='room_no_1').all()
    return render_template('room_no_1.html',
                           daily_records=daily_records,
                           monthly_records=monthly_records,
                           yearly_records=yearly_records)

@app.route('/logging_section')
def logging_section():
    daily_records = DailyBackup.query.filter_by(backup_type='logging_section').all()
    monthly_records = MonthlyBackup.query.filter_by(backup_type='logging_section').all()
    yearly_records = YearlyBackup.query.filter_by(backup_type='logging_section').all()
    return render_template('logging_section.html',
                           daily_records=daily_records,
                           monthly_records=monthly_records,
                           yearly_records=yearly_records)

@app.route('/corporate_eds')
def corporate_eds():
    daily_records = DailyBackup.query.filter_by(backup_type='corporate_eds').all()
    monthly_records = MonthlyBackup.query.filter_by(backup_type='corporate_eds').all()
    yearly_records = YearlyBackup.query.filter_by(backup_type='corporate_eds').all()
    return render_template('corporate_eds.html',
                           daily_records=daily_records,
                           monthly_records=monthly_records,
                           yearly_records=yearly_records)


# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True)
