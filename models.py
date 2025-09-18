# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt

# db = SQLAlchemy()
# bcrypt = Bcrypt()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)  # Hashed password
#     role = db.Column(db.String(10), nullable=False)  # 'admin' or 'user'

#     def set_password(self, password):
#         self.password = bcrypt.generate_password_hash(password).decode('utf-8')

#     def check_password(self, password):
#         return bcrypt.check_password_hash(self.password, password)















# class BackupRecord(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     backup_type = db.Column(db.String(50), nullable=False)  # e.g., 'nas', 'logging_section', etc.
#     backup_frequency = db.Column(db.String(20), nullable=False)  # 'daily', 'monthly', or 'yearly'
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
#                  backup_format, backup_media, remarks=None, tape_reuse_date=None, extra_info=None):
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
