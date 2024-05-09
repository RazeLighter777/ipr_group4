from flask import Flask, render_template_string, request, session, redirect, url_for
import os
from flask_mysqldb import MySQL
from flask_session import Session
import MySQLdb.cursors
import redis
import password_gen
app = Flask(__name__)

# Get the connection details from the environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DATABASE'] = os.environ.get('MYSQL_DATABASE')
app.config['REDIS_HOST'] = os.environ.get('REDIS_HOST')
app.config['SESSION_REDIS'] = redis.Redis(host=app.config['REDIS_HOST'])
app.config['SESSION_TYPE'] = 'redis'

app.secret_key = os.environ.get('SECRET_KEY', default='supersecretkey')

server_session = Session(app)


mysql =  MySQL(app)




@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'




@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    is_writer = request.form.get('is_writer', False)
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, password_hash, is_writer) VALUES (%s, %s, %s)", (username, password_gen.hash_password(password), is_writer))
    mysql.connection.commit()
    cur.close()
    return redirect("/login.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cur.fetchone()
    cur.close()
    if user is not None and password_gen.check_password(password, user['password_hash']):
        session['user_id'] = user['id']
        return redirect("/dashboard.html")
    else:
        return 'Invalid username or password'


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')