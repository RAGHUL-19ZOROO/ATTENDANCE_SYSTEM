from flask import Blueprint
from flask import render_template, request, redirect
from db import get_db_connection 
from datetime import date


rep_dash_bp = Blueprint(
    "rep_dash",
    __name__,
    
)




# @rep_dash_bp.route("/dash")
# def dashboard():
#     db = get_db_connection()
#     cursor = db.cursor(dictionary=True)

#     cursor.execute("SELECT * FROM students")
#     students = cursor.fetchall()
    

#     return render_template("dashboard.html", students=students)


# @rep_dash_bp.route("/save", methods=["POST"])
# def save_attendance():
#     db = get_db_connection()
#     cursor = db.cursor()
     

#     date = request.form.get("date")

#     for key in request.form:
#         if key.startswith("status_"):
#             student_id = key.split("_")[1]
#             status = request.form[key]

#             cursor.execute("SELECT student_name FROM students WHERE student_id = %s", (student_id,))
#             student_name = cursor.fetchone()[0]

#             cursor.execute("""
#                 INSERT INTO attendance (student_id,student_name, date, status)
#                 VALUES (%s,%s,%s,%s)
#             """, (student_id, student_name, date, status))

#     db.commit()
#     return render_template("dashboard.html")



@rep_dash_bp.route("/dash")
def dashboard():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    selected_date = request.args.get("date")

    if not selected_date:
        selected_date = str(date.today())

    # get students
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    # 🔴 check if attendance already saved for this date
    cursor.execute(
        "SELECT COUNT(*) as count FROM attendance WHERE date=%s",
        (selected_date,)
    )
    result = cursor.fetchone()
    locked = result["count"] > 0

    return render_template(
        "dashboard.html",
        students=students,
        selected_date=selected_date,
        locked=locked
    )


@rep_dash_bp.route("/save", methods=["POST"])
def save_attendance():
    db = get_db_connection()
    cursor = db.cursor()

    selected_date = request.form.get("date")

    # 🔴 prevent saving again
    cursor.execute(
        "SELECT COUNT(*) FROM attendance WHERE date=%s",
        (selected_date,)
    )
    if cursor.fetchone()[0] > 0:
        return redirect("/dash")

    for key in request.form:
        if key.startswith("status_"):
            student_id = key.split("_")[1]
            status = request.form[key]

            cursor.execute(
                "SELECT student_name FROM students WHERE student_id=%s",
                (student_id,)
            )
            student_name = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO attendance (student_id, student_name, date, status)
                VALUES (%s,%s,%s,%s)
            """, (student_id, student_name, selected_date, status))

    db.commit()
    return redirect("/dash")
