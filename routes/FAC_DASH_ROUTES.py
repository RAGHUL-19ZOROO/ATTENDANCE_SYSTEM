from flask import Blueprint, render_template
from db import get_db_connection
from datetime import date

admin_dash = Blueprint("admin_dash", __name__)

@admin_dash.route("/admin_dashboard")
@admin_dash.route("/admin_dashboard")
def admin_dashboard():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    today = str(date.today())

    # ===============================
    # GET STUDENTS + TODAY ATTENDANCE
    # ===============================
    cursor.execute("""
    SELECT students.student_id,
           students.student_name,
           attendance.p1,
           attendance.p2,
           attendance.p3,
           attendance.p4,
           attendance.p5,
           attendance.p6,
           attendance.p7,
           attendance.p8
    FROM students
    LEFT JOIN attendance
    ON students.student_id = attendance.student_id
    AND attendance.date=%s
    """,(today,))

    data = cursor.fetchall()

    total_students = len(data)

    # ===============================
    # FIND LATEST FILLED PERIOD
    # ===============================
    period_order = ["p8","p7","p6","p5","p4","p3","p2","p1"]
    latest_period = None

    for p in period_order:
        for row in data:
            if row[p] is not None:
                latest_period = p
                break
        if latest_period:
            break

    present = 0
    absent = 0

    if latest_period:
        for row in data:
            if row[latest_period] == "P":
                present += 1
            elif row[latest_period] == "A":
                absent += 1

    # ===============================
    # ABSENT LIST
    # ===============================
    absentees = []
    if latest_period:
        for row in data:
            if row[latest_period] == "A":
                absentees.append(row)

    return render_template(
        "ADMIN_DASHBOARD.html",
        total=total_students,
        present=present,
        absent=absent,
        period=latest_period if latest_period else "No hour yet",
        absentees=absentees,
        today=today
    )

