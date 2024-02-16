from flask import Flask, render_template, request, redirect
import pymysql 
import pymysql.cursors
import flask_login
from flask import g

app = Flask(__name__)
app.secret_key = "yabadabado beat drop"
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User:
       is_authenticated = True
       is_anonymous = False
       is_active = True

       def __init__(self, id, useename):
              self.id = id
              return str(self.id)
       @login_manager.user_loader
       def load_user(user_id):
             cursor = get_db().cursor()
             cursor.execute("SELECT * FROM `users` WHERE `id` = " + user_id)
             result = cursor.fetchone()
             cursor.close()
             cursor.commit()
             if result is None:
                   return None
             return User(result["id"], ["username"])
       
@app.route('/')
def index():
    return render_template('landing.html.jinja')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor = get_db().cursor()
        cursor.execute(f'INSERT INTO `users` (`username`, `email`, `password`) VALUES ("{username}", "{email}", "{password}");')
        cursor.close()
        get_db().commit()
    return render_template('signup.html.jinja')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = get_db().cursor()
        cursor.execute(f'SELECT * FROM `users` WHERE `username` = "{username}"')
        result = cursor.fetchone()
        if password == result['password']:
            user = user (result['id'])
            flask_login.login_user(user)
            return redirect('/feed')
    return render_template('signin.html.jinja')

@app.route('/feed')
@flask_login.login_required
def feed():
    return render_template('feed.html.jinja')

@app.route('/new')
def landing():
    return render_template('landing.html.jinja')

@app.route('/post', methods=['POST'])
@flask_login.login_required
def create_post():
    description = request.form['description']
    user_id = flask_login.current_user.id

    cursor = get_db().cursor()

    cursor.execute("INSERT INTO `posts` (`description`, `user_id`)")

    def connect_db():
        return pymysql.connect(
         host="10.100.33.60",
         user="svassell",
         password="228426979",
         database="Sham_Shack",
         cursorclass=pymysql.cursors.DictCursor,
         autocommit=True
    )

def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        cursor = get_db().cursor()

    return g.db    

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(g, 'db'):
        g.db.close() 