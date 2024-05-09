from flask import Flask, render_template_string, request, session, redirect, url_for
from markupsafe import escape
import os
from flask_mysqldb import MySQL
from flask_session import Session
import MySQLdb.cursors
import password_gen
app = Flask(__name__)

# Get the connection details from the environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DATABASE')
app.secret_key = os.environ.get('SECRET_KEY', default='supersecretkey')
app.config["SESSION_TYPE"] = "cachelib"
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
    cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (escape(username), password_gen.hash_password(password)))
    mysql.connection.commit()
    cur.close()
    return redirect("/login.html")


@app.route('/my_username')
def my_username():
    #check if user is logged in, if not return guest
    if 'user_id' not in session:
        return {'username': "Guest"}
    cur = mysql.connection.cursor()
    cur.execute("SELECT username FROM users WHERE id=%s", (session['user_id'],))
    username = cur.fetchone()[0]
    cur.close()
    return {'username': username}

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    user = cur.fetchone()
    cur.close()
    if user is not None and password_gen.check_password(password, user[2]):
        session['user_id'] = user[0]
        return redirect("/index.html")
    else:
        return 'Invalid username or password'

@app.route('/create_post', methods=['POST'])
def create_post():
    #check if user is logged in, if not redirect to login
    if 'user_id' not in session:
        return redirect("/login.html")
    title = request.form['title']
    content = request.form['content']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO posts (title, content, user_id) VALUES (%s, %s, %s)", (title, content, session['user_id']))
    mysql.connection.commit()
    cur.close()
    return redirect("/index.html")

@app.route('/delete_post', methods=['POST'])
def delete_post():
    #check if user is logged in, if not redirect to login
    if 'user_id' not in session:
        return redirect("/login.html")
    #get json data
    post_id = request.json['post_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id FROM posts WHERE id=%s", (post_id,))
    post = cur.fetchone()
    cur.close()
    #check if post exists
    if post is None:
        return { success: False, error: "Post does not exist" }
    #check if user is the author of the post
    if post[0] != session['user_id']:
        return { success: False, error: "You are not the author of this post" }
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM posts WHERE id=%s", (post_id,))
    mysql.connection.commit()
    cur.close()
    return { success: True }


@app.route('/get_posts')
def get_posts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    cur.close()
    posts_with_username = []
    for post in posts:
        #add username to each post
        cur = mysql.connection.cursor()
        cur.execute("SELECT username FROM users WHERE id=%s", (post[3],))
        username = cur.fetchone()[0]
        cur.close()
        posts_with_username.append({'title': post[1], 'content': post[2], 'username': username, 'id': post[0]})
        #sanitize content and title
        for post in posts_with_username:
            post['title'] = escape(post['title'])
            post['content'] = escape(post['content'])

    return {'posts': posts_with_username}

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')