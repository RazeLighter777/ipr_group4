from flask import Flask, render_template_string, request, session, redirect, url_for
import os
from flask_mysqldb import MySQL
from flask_session import Session
import MySQLdb.cursors
app = Flask(__name__)

# Get the connection details from the environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DATABASE'] = os.environ.get('MYSQL_DATABASE')

app.secret_key = os.environ.get('SECRET_KEY', default='supersecretkey')

def init_mysql():
    return MySQL(app)

mysql = init_mysql()




@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')