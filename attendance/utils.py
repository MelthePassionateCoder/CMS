import pandas as pd
from student.models import Student
from .models import DailyAttendance

def process_attendance_file(file, advisory_id, date):
    try:
        df = pd.read_excel(file)

        for index, row in df.iterrows():
            lrn = str(row['LRN'])

            student, created = Student.objects.get_or_create(lrn=lrn)

            attendance, created = DailyAttendance.objects.get_or_create(
                advisory_id=advisory_id,
                student=student,
                date=date
            )

            attendance.morning_in_status = row['Morning In']
            attendance.morning_out_status = row['Morning Out']
            attendance.afternoon_in_status = row['Afternoon In']
            attendance.afternoon_out_status = row['Afternoon Out']

            attendance.save()

        return True, None  
    except Exception as e:
        return False, str(e) 