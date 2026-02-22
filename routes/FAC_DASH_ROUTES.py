from flask import Blueprint, render_template, request,session, redirect
from db import get_db_connection
from datetime import date

admin_dash = Blueprint("admin_dash", __name__)

@admin_dash.route("/admin_dashboard")
def admin_dashboard():

    if "hod_dept" not in session:
        return redirect("/FAC")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    today = str(date.today())

    # dept locked from login
    dept = session["hod_dept"]

    # year filter from dropdown
    year = request.args.get("year")

    params = [today, dept]

    year_filter = ""
    if year:
        year_filter = "AND students.year=%s"
        params.append(year)

    query = f"""
    SELECT students.student_id,
           students.student_name,
           students.year,
           attendance.p1,attendance.p2,attendance.p3,attendance.p4,
           attendance.p5,attendance.p6,attendance.p7,attendance.p8
    FROM students
    LEFT JOIN attendance
    ON students.student_id = attendance.student_id
    AND attendance.date=%s
    WHERE students.department=%s
    {year_filter}
    """

    cursor.execute(query, tuple(params))
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

    absentees = [row for row in data if latest_period and row[latest_period]=="A"]

    return render_template(
        "ADMIN_DASHBOARD.html",
        total=total_students,
        present=present,
        absent=absent,
        period=latest_period if latest_period else "-",
        absentees=absentees,
        selected_year=year,
        dept=dept
    )
    
    
    
@admin_dash.route("/student_percentage")
def student_percentage():

    if "hod_dept" not in session:
        return redirect("/FAC")

    dept = session["hod_dept"]
    year = request.args.get("year")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    params = [dept]
    year_filter = ""

    if year:
        year_filter = "AND year=%s"
        params.append(int(year))

    cursor.execute(f"""
        SELECT student_id, student_name
        FROM students
        WHERE department=%s
        {year_filter}
    """, tuple(params))

    students = cursor.fetchall()

    results = []

    for s in students:
        cursor.execute("""
            SELECT p1,p2,p3,p4,p5,p6,p7,p8
            FROM attendance
            WHERE student_id=%s
        """,(s["student_id"],))

        records = cursor.fetchall()

        total_classes = 0
        total_present = 0

        for r in records:
            for p in ["p1","p2","p3","p4","p5","p6","p7","p8"]:
                if r[p] is not None:
                    total_classes += 1
                    if r[p] == "P":
                        total_present += 1

        percent = round((total_present/total_classes)*100,2) if total_classes else 0

        results.append({
            "student_id": s["student_id"],
            "student_name": s["student_name"],
            "percentage": percent
        })

    return render_template(
        "STUDENT_PERCENTAGE.html",
        students=results,
        dept=dept,
        year=year
    )