from flask import Blueprint, render_template, request, session, redirect
from db import get_db_connection
from datetime import date

staff_dash = Blueprint("staff_dash", __name__)

@staff_dash.route("/staff_dash", methods=["GET"])
def staff_dashboard():

    if "staff_user" not in session:
        return redirect("/staff")

    dept = request.args.get("dept")
    year = request.args.get("year")

    today = str(date.today())

    today_absentees = []
    long_absentees = []
    latest_period = None

    if dept and year:

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        # today's attendance
        cursor.execute("""
        SELECT students.student_id,
               students.student_name,
               attendance.p1,attendance.p2,attendance.p3,attendance.p4,
               attendance.p5,attendance.p6,attendance.p7,attendance.p8
        FROM students
        LEFT JOIN attendance
        ON students.student_id = attendance.student_id
        AND attendance.date=%s
        WHERE students.department=%s AND students.year=%s
        """, (today, dept, int(year)))

        data = cursor.fetchall()

        # find latest period
        for p in ["p8","p7","p6","p5","p4","p3","p2","p1"]:
            if any(r[p] is not None for r in data):
                latest_period = p
                break

        if latest_period:
            for r in data:
                if r[latest_period] == "A":
                    today_absentees.append(r)

        # long absentees (<75%)
        cursor.execute("""
        SELECT student_id, student_name
        FROM students
        WHERE department=%s AND year=%s
        """, (dept, int(year)))

        students = cursor.fetchall()

        for s in students:
            cursor.execute("""
            SELECT p1,p2,p3,p4,p5,p6,p7,p8
            FROM attendance
            WHERE student_id=%s
            """, (s["student_id"],))

            records = cursor.fetchall()

            total = 0
            present = 0

            for rec in records:
                for val in rec.values():
                    if val is not None:
                        total += 1
                        if val == "P":
                            present += 1

            if total > 0:
                percent = (present / total) * 100
                if percent < 75:
                    long_absentees.append({
                        "student_name": s["student_name"],
                        "percent": round(percent, 2)
                    })

        cursor.close()
        db.close()

    return render_template(
        "STAFF_DASH.html",
        dept=dept,
        year=year,
        today_absentees=today_absentees,
        long_absentees=long_absentees,
        period=latest_period
    )