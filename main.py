from flask import Flask
from flask import render_template
import pymysql

app = Flask(__name__)
conn = pymysql.connect(
    database = "svassell_Sham_Shack",
    user = "svassell2",
    password = "228426979",
    host = "10.100.33.60",
    cursorclass = pymysql.cursors.DictCursor

)

@app.route('/')
def index():
    return render_template("home.html.jinja")

@app.route('/signup')
def signup():
    return render_template('Signup.html.jinja')