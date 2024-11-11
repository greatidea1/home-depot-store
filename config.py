# config.py

import os

# MySQL database connection details
DB_HOST = 'your-remote-mysql-server.com'
DB_USER = 'your-username'
DB_PASSWORD = 'your-password'
DB_NAME = 'your_db_name'

# SQLAlchemy database URI for connecting to MySQL database
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
