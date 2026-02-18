from flask import Blueprint, redirect, render_template, request
from db import get_db_connection

FAC_auth = Blueprint("FAC_auth", __name__)



@FAC_auth.route("/FAC", methods=["GET","POST"])
def Fac_login():

    if request.method == "GET":
        return render_template("FAC_LOGIN.html")

    username = request.form.get("username")
    password = request.form.get("password")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM faculty_log WHERE username=%s AND password=%s",
        (username, password)
    )

    admin = cursor.fetchone()
    cursor.close()
    db.close()

    if admin:
        return redirect("/admin_dashboard")
    else:
        msg = "Invalid credentials"
        return render_template("ADMIN_LOGIN.html", msg=msg)


   
