from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Attendance, Marks, Accounts, Student_Profile,Feedback,Faculty_Feedback,Departments,Students,Faculty,Faculty_Profile

# Create an engine and bind it to the Base class
engine = create_engine('sqlite:///database1.db')
Base.metadata.bind = engine

# Create a session
DBSession = sessionmaker(bind=engine)
db = DBSession()

db.query(Student_Profile).filter(Student_Profile.dob == '').update({Student_Profile.dob: None}, synchronize_session=False)

# Commit the changes
db.commit()
print('**********************************')


new_account = Accounts(id='new_id_here', name='New Name', user_type='user', password='secret_password')

# Add the new record to the session
db.add(new_account)

# Commit the changes to the database
db.commit()

# Close the session
db.close()
# Querying the Accounts table and printing data
account_records = db.query(Accounts).all()
if account_records:
    for account in account_records:
        print(f"Account ID: {account.id}, User Type: {account.user_type}")
else:
    print("No accounts found.")

# Close the session
db.close()
