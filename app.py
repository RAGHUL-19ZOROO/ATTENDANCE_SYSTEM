from flask import Flask, render_template
from routes.REP_AUTH_ROUTES import REP_auth
from routes.REP_DASH_ROUTES import rep_dash_bp
from routes.FAC_AUTH_ROUTES import FAC_auth
from routes.FAC_DASH_ROUTES import admin_dash
from routes.fetch_stud_auth import fetch_bp
from routes.EXPORT_ROUTES import export_bp
import os
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy








app=Flask(__name__)
app.secret_key = "attendance_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

app.register_blueprint(REP_auth)
app.register_blueprint(rep_dash_bp)
app.register_blueprint(FAC_auth)

app.register_blueprint(admin_dash)
app.register_blueprint(fetch_bp)

app.register_blueprint(export_bp)
    
@app.route("/")
def index():
    return render_template('HOME_PAGE.html')
@app.route("/replogin")
def replogin():
    return render_template("REP_LOGIN.html")
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html",data="Welcome to the dashboard!")
@app.route("/faclogin")
def faclogin():
    return render_template("ADMIN_LOGIN.html")
@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("ADMIN_DASHBOARD.html",data="Welcome to the Admin dashboard!")
@app.route("/fetch_students")
def fetch_students():
    return render_template("STUDENTS.html",data="Welcome to the Admin dashboard!")
@app.route("/stafflogin")
def stafflogin():
    return render_template("STAFF_LOGIN.html")
@app.route("/staff_dashboard")
def staff_dashboard():  
    return render_template("staff_dashboard.html",data="Welcome to the Staff dashboard!")



if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0', port=5000)  


    
    
    