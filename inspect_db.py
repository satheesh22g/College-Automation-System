from database import *
from sqlalchemy import inspect

engine = create_engine('sqlite:///database.db')
inspector = inspect(engine)

print('\n' + '='*60)
print('DATABASE SCHEMA ANALYSIS')
print('='*60 + '\n')

tables = inspector.get_table_names()
for table in tables:
    print(f'\n📊 TABLE: {table.upper()}')
    print('-' * 60)
    columns = inspector.get_columns(table)
    for col in columns:
        print(f'  ├─ {col["name"]:25} : {col["type"]}')

print('\n' + '='*60)
print('SAMPLE DATA')
print('='*60 + '\n')

# Check sample data
db = DBSession()

# Accounts
print('\n👥 ACCOUNTS:')
accounts = db.query(Accounts).limit(3).all()
for acc in accounts:
    print(f'  ├─ {acc.id} ({acc.user_type}): {acc.name}')

# Students
print('\n🎓 STUDENTS:')
students = db.query(Student_Profile).limit(3).all()
for stu in students:
    print(f'  ├─ {stu.sid}: {stu.name} ({stu.branch})')

# Faculty
print('\n👨‍🏫 FACULTY:')
faculty = db.query(Faculty).limit(3).all()
for fac in faculty:
    print(f'  ├─ {fac.id}: {fac.name}')

# Attendance
print('\n📋 ATTENDANCE:')
attend = db.query(Attendance).limit(3).all()
for att in attend:
    print(f'  ├─ Student: {att.student_id}, Attendance: {att.attend_perc}%')

# Marks
print('\n📊 MARKS:')
marks = db.query(Marks).limit(3).all()
for mark in marks:
    print(f'  ├─ Student: {mark.student_id}, Average: {mark.average}%')

print('\n' + '='*60)
