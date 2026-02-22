from flask import Blueprint, render_template, request, redirect, session
from db import get_db_connection

staff_auth = Blueprint("staff_auth", __name__)

@staff_auth.route("/staff", methods=["GET", "POST"])
def staff_login():

    # If already logged in → go dashboard
    if "staff_user" in session:
        return redirect("/staff_dash")

    if request.method == "GET":
        return render_template("STAFF_LOGIN.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return render_template("STAFF_LOGIN.html", msg="Enter username and password")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM staff_log
        WHERE username=%s AND password=%s
    """, (username, password))

    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user:
        session["staff_user"] = user["username"]
        return redirect("/staff_dash")

    return render_template("STAFF_LOGIN.html", msg="Invalid login")