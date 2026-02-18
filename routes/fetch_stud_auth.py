from flask import Blueprint, render_template, request
from db import get_db_connection

fetch_bp = Blueprint("fetch_stud", __name__)

@fetch_bp.route("/fetch", methods=["GET","POST"])
def view_students():

    students = []
    selected_date = None
    selected_hour = None
    percent = 0

    if request.method == "POST":
        selected_date = request.form.get("date")
        selected_hour = request.form.get("hour")

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        query = """
        SELECT students.student_id,
               students.student_name,
               attendance.p1,attendance.p2,attendance.p3,attendance.p4,
               attendance.p5,attendance.p6,attendance.p7,attendance.p8
        FROM students
        LEFT JOIN attendance
        ON students.student_id = attendance.student_id
        AND attendance.date=%s
        """

        cursor.execute(query,(selected_date,))
        students = cursor.fetchall()

        total_students = len(students)

        # ===== FULL DAY % =====
        if not selected_hour:
            total_present = 0
            for s in students:
                periods = [
                    s["p1"],s["p2"],s["p3"],s["p4"],
                    s["p5"],s["p6"],s["p7"],s["p8"]
                ]
                total_present += periods.count("P")

            total_possible = total_students * 8
            percent = round((total_present/total_possible)*100) if total_possible else 0

        # ===== SINGLE HOUR % =====
        else:
            present = 0
            for s in students:
                if s[selected_hour] == "P":
                    present += 1

            percent = round((present/total_students)*100) if total_students else 0

    return render_template(
        "STUDENTS.html",
        students=students,
        selected_date=selected_date,
        selected_hour=selected_hour,
        percent=percent
    )
