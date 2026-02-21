
from flask import Blueprint, send_file, request
from db import get_db_connection
from datetime import date, timedelta
import pandas as pd
import io
staff_bp = Blueprint("staff_auth", __name__)






@staff_bp.route("/staff_dashboard", methods=["GET","POST"])
def staff_dashboard():
    student=None
    percentage=0
    attendance_records=[]

    if request.method=="POST":
        reg_no=request.form["reg_no"]

        student=Student.query.filter_by(register_no=reg_no).first()

        if student:
            records=Attendance.query.filter_by(student_id=student.id).all()
            attendance_records=records

            total=len(records)
            present=len([r for r in records if r.status=="Present"])

            if total>0:
                percentage=round((present/total)*100,2)

    return render_template(
        "staff_dashboard.html",
        student=student,
        percentage=percentage,
        attendance_records=attendance_records
    )