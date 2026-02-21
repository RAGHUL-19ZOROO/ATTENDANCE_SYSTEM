from flask import Blueprint, redirect, render_template, request, session
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
        # 🔐 dept only from DB
        session["dept"] = admin["department"]
        session["year"] = "2"

        print("Logged dept:", admin["department"])

        return redirect("/dash")

    else:
        msg="Invalid credentials"
        return render_template("REP_LOGIN.html", msg=msg)