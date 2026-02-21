from flask import Blueprint, send_file, request
from db import get_db_connection
from datetime import date, timedelta
import pandas as pd
import io

from io import BytesIO

export_bp = Blueprint("export_bp", __name__)


def get_last_period(rows):
    order = ["p8","p7","p6","p5","p4","p3","p2","p1"]
    for p in order:
        for r in rows:
            if r[p] is not None:
                return p
    return None
    




@export_bp.route("/export/day")
def export_day():
    selected_date = request.args.get("date")

    if not selected_date:
        return "No date selected"

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
    """,(selected_date,))

    data = cursor.fetchall()

    df = pd.DataFrame(data)
    df = df.rename(columns={
    "p1": "Period 1",
    "p2": "Period 2",
    "p3": "Period 3",
    "p4": "Period 4",
    "p5": "Period 5",
    "p6": "Period 6",
    "p7": "Period 7",
    "p8": "Period 8"
})


    output = BytesIO()
    df.to_excel(output,index=False)
    output.seek(0)

    return send_file(output,
        download_name=f"Attendance_{selected_date}.xlsx",
        as_attachment=True)



@export_bp.route("/export/last")
def export_last():
    selected_date = request.args.get("date")

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM attendance WHERE date=%s
    """,(selected_date,))
    rows = cursor.fetchall()

    last_period = None
    for p in ["p8","p7","p6","p5","p4","p3","p2","p1"]:
        if any(r[p] is not None for r in rows):
            last_period = p
            break

    if not last_period:
        return "No attendance yet"

    cursor.execute(f"""
        SELECT students.student_id,
               students.student_name,
               attendance.{last_period} as status
        FROM students
        LEFT JOIN attendance
        ON students.student_id = attendance.student_id
        AND attendance.date=%s
    """,(selected_date,))

    data = cursor.fetchall()

    df = pd.DataFrame(data)
    df = df.rename(columns={
   
    "p8": "Period 8"
})


    output = BytesIO()
    df.to_excel(output,index=False)
    output.seek(0)

    return send_file(output,
        download_name=f"LastHour_{selected_date}.xlsx",
        as_attachment=True)



@export_bp.route("/export/week")
def export_week():

    start = request.args.get("start")  # monday date

    start_date = date.fromisoformat(start)
    end_date = start_date + timedelta(days=6)

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
    SELECT * FROM attendance
    WHERE date BETWEEN %s AND %s
    """,(start_date, end_date))

    rows = cursor.fetchall()

    df = pd.DataFrame(rows)
    df = df.rename(columns={
    "p1": "Period 1",
    "p2": "Period 2",
    "p3": "Period 3",
    "p4": "Period 4",
    "p5": "Period 5",
    "p6": "Period 6",
    "p7": "Period 7",
    "p8": "Period 8"
})


    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(output,
        download_name="weekly_attendance.xlsx",
        as_attachment=True)



@export_bp.route("/export/month")
def export_month():

    month = request.args.get("month") 

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
    SELECT * FROM attendance
    WHERE DATE_FORMAT(date,'%%Y-%%m')=%s
    """,(month,))

    rows = cursor.fetchall()

    df = pd.DataFrame(rows)
    df = df.rename(columns={
    "p1": "Period 1",
    "p2": "Period 2",
    "p3": "Period 3",
    "p4": "Period 4",
    "p5": "Period 5",
    "p6": "Period 6",
    "p7": "Period 7",
    "p8": "Period 8"
})


    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(output,
        download_name="monthly_attendance.xlsx",
        as_attachment=True)
