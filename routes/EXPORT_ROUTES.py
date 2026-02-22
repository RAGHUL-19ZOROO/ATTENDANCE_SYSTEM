from flask import Blueprint, send_file, request, session, redirect
from db import get_db_connection
import pandas as pd
from datetime import date

export_bp = Blueprint("export", __name__)

# ===== DAY EXPORT =====
@export_bp.route("/export/day")
def export_day():

    if "hod_dept" not in session:
        return redirect("/FAC")

    dept = session["hod_dept"]
    selected_date = request.args.get("date")

    if not selected_date:
        selected_date = str(date.today())

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
    SELECT students.student_id,
           students.student_name,
           attendance.p1,attendance.p2,attendance.p3,attendance.p4,
           attendance.p5,attendance.p6,attendance.p7,attendance.p8
    FROM students
    LEFT JOIN attendance
    ON students.student_id = attendance.student_id
    AND attendance.date=%s
    WHERE students.department=%s
    """,(selected_date, dept))

    data = cursor.fetchall()
    df = pd.DataFrame(data)
    file="day.xlsx"
    df.to_excel(file,index=False)

    return send_file(file,as_attachment=True)


# ===== MONTH EXPORT =====
@export_bp.route("/export/month")
def export_month():

    if "hod_dept" not in session:
        return redirect("/FAC")

    dept = session["hod_dept"]
    month = request.args.get("month")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
    SELECT students.student_id,
           students.student_name,
           attendance.date,
           attendance.p1,attendance.p2,attendance.p3,attendance.p4,
           attendance.p5,attendance.p6,attendance.p7,attendance.p8
    FROM students
    JOIN attendance
    ON students.student_id = attendance.student_id
    WHERE students.department=%s
    AND DATE_FORMAT(attendance.date,'%%Y-%%m')=%s
    """,(dept, month))

    data = cursor.fetchall()
    df = pd.DataFrame(data)
    file="month.xlsx"
    df.to_excel(file,index=False)

    return send_file(file,as_attachment=True)