from flask import Blueprint, render_template, request, redirect, session
from db import get_db_connection
from datetime import date, timedelta

rep_dash_bp = Blueprint("rep_dash", __name__)

@rep_dash_bp.route("/dash")
def dashboard():

    if "dept" not in session:
        return redirect("/REP")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    selected_date = request.args.get("date")
    selected_period = request.args.get("period")

    if not selected_period:
        selected_period = "p1"

    if not selected_date:
        selected_date = str(date.today())

    dept = session.get("dept")
    year = session.get("year")

    print("SESSION:", dept, year)

    query = """
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
    WHERE students.department=%s
    AND students.year=%s
    """

    cursor.execute(query, (selected_date, dept, year))
    students = cursor.fetchall()

    today = date.today()
    yesterday = today - timedelta(days=1)
    selected_date_obj = date.fromisoformat(selected_date)

    editable = selected_date_obj in [today, yesterday]
    locked = not editable

    return render_template(
        "dashboard.html",
        students=students,
        selected_date=selected_date,
        selected_period=selected_period,
        locked=locked,
        dept=dept,
        year=year
    )
    
@rep_dash_bp.route("/save", methods=["POST"])
def save():

    if "dept" not in session:
        return redirect("/REP")

    dept = session.get("dept")
    year = session.get("year")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    selected_date = request.form.get("date")
    period = request.form.get("period")
    copy_prev = request.form.get("copy_prev")

    if not period:
        return redirect("/dash?date=" + selected_date)

    # ================= COPY PREVIOUS =================
    if copy_prev == "1":

        prev_map = {
            "p2": "p1",
            "p3": "p2",
            "p4": "p3",
            "p5": "p4",
            "p6": "p5",
            "p7": "p6",
            "p8": "p7"
        }

        if period in prev_map:

            prev_col = prev_map[period]

            # get only this class students
            cursor.execute("""
                SELECT student_id
                FROM students
                WHERE department=%s AND year=%s
            """,(dept, year))

            students = cursor.fetchall()

            for s in students:
                sid = s["student_id"]

                # get previous period value
                cursor.execute(f"""
                    SELECT {prev_col}
                    FROM attendance
                    WHERE student_id=%s AND date=%s
                """,(sid, selected_date))

                prev = cursor.fetchone()

                if prev and prev[prev_col] is not None:

                    # check if today's row exists
                    cursor.execute("""
                        SELECT id FROM attendance
                        WHERE student_id=%s AND date=%s
                    """,(sid, selected_date))

                    exists = cursor.fetchone()

                    if exists:
                        cursor.execute(f"""
                            UPDATE attendance
                            SET {period}=%s
                            WHERE student_id=%s AND date=%s
                        """,(prev[prev_col], sid, selected_date))
                    else:
                        cursor.execute(f"""
                            INSERT INTO attendance (student_id,date,{period})
                            VALUES (%s,%s,%s)
                        """,(sid, selected_date, prev[prev_col]))

        db.commit()
        return redirect(f"/dash?date={selected_date}&period={period}")

    # ================= NORMAL SAVE =================
    for key in request.form:
        if key.startswith("status_"):
            student_id = key.split("_")[1]
            status = request.form[key]

            # ensure correct class
            cursor.execute("""
                SELECT student_id FROM students
                WHERE student_id=%s AND department=%s AND year=%s
            """,(student_id, dept, year))

            valid = cursor.fetchone()
            if not valid:
                continue

            cursor.execute("""
                SELECT id FROM attendance
                WHERE student_id=%s AND date=%s
            """,(student_id, selected_date))

            exists = cursor.fetchone()

            if exists:
                cursor.execute(f"""
                    UPDATE attendance
                    SET {period}=%s
                    WHERE student_id=%s AND date=%s
                """,(status, student_id, selected_date))
            else:
                cursor.execute(f"""
                    INSERT INTO attendance (student_id,date,{period})
                    VALUES (%s,%s,%s)
                """,(student_id, selected_date, status))

    db.commit()
    return redirect(f"/dash?date={selected_date}&period={period}")