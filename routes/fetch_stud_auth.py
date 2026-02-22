from flask import Blueprint, render_template, request, session, redirect
from db import get_db_connection
from datetime import date

fetch_bp = Blueprint("fetch_stud", __name__)

@fetch_bp.route("/fetch", methods=["GET","POST"])
def view_students():

    if "hod_dept" not in session:
        return redirect("/FAC")

    students = []
    selected_date = request.values.get("date")
    year = request.values.get("year")
    dept = session["hod_dept"]

    if not selected_date:
        selected_date = str(date.today())

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    params = [selected_date, dept]

    if year:
        query = """
        SELECT students.student_id,
               students.student_name,
               attendance.p1,attendance.p2,attendance.p3,attendance.p4,
               attendance.p5,attendance.p6,attendance.p7,attendance.p8
        FROM students
        LEFT JOIN attendance
        ON students.student_id = attendance.student_id
        AND attendance.date=%s
        WHERE students.department=%s
        AND students.year=%s
        """
        params.append(int(year))
    else:
        query = """
        SELECT students.student_id,
               students.student_name,
               attendance.p1,attendance.p2,attendance.p3,attendance.p4,
               attendance.p5,attendance.p6,attendance.p7,attendance.p8
        FROM students
        LEFT JOIN attendance
        ON students.student_id = attendance.student_id
        AND attendance.date=%s
        WHERE students.department=%s
        """

    cursor.execute(query, tuple(params))
    students = cursor.fetchall()

    return render_template(
        "STUDENTS.html",
        students=students,
        selected_date=selected_date,
        year=year,
        dept=dept
    )