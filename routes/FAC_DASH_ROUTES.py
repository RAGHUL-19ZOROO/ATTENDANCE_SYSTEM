from flask import Blueprint, render_template, request
from db import get_db_connection
from datetime import date

admin_dash = Blueprint("admin_dash", __name__)

@admin_dash.route("/admin_dashboard")
def admin_dashboard():

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    today = str(date.today())

    dept = request.args.get("dept")

    if dept:
        dept_filter = "WHERE students.department=%s"
        params = (today, dept)
    else:
        dept_filter = ""
        params = (today,)

    query = f"""
    SELECT students.student_id,
           students.student_name,
           students.department,
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
    {dept_filter}
    """

    cursor.execute(query, params)
    data = cursor.fetchall()

    total_students = len(data)

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

    overall_percent = round((present / total_students) * 100, 2) if total_students > 0 else 0

    absentees = [row for row in data if latest_period and row[latest_period] == "A"]

    return render_template(
        "ADMIN_DASHBOARD.html",
        total=total_students,
        present=present,
        absent=absent,
        period=latest_period if latest_period else "No hour yet",
        absentees=absentees,
        overall_percent=overall_percent,
        selected_dept=dept
    )