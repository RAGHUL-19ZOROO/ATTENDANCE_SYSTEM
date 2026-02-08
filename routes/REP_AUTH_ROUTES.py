from flask import Blueprint, redirect, render_template, request
from db import get_db_connection

REP_auth = Blueprint("REP_auth", __name__)

@REP_auth.route("/REP", methods=["GET", "POST"])
def Rep_login():
    msg=None
    
    if request.method == "GET":
        return render_template("REP_LOGIN.html")

   
    username = request.form.get("username")
    password = request.form.get("password")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM rep_log WHERE username=%s AND password=%s",
        (username, password)
    )
    admin = cursor.fetchone()
    cursor.close()
    db.close()

    if admin:
        msg="Login successful!"
        return redirect("/dash")
    else:
        msg="Invalid credentials. Please try again."
        return render_template("REP_LOGIN.html", msg=msg)


   
