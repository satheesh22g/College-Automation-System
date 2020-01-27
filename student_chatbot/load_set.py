import sys
import csv
import os
from database import Base, Attendance, Marks, Accounts, Profile
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine('sqlite:///database.db',connect_args={'check_same_thread': False},echo=True)
Base.metadata.bind = engine
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("attend.csv")
    reader = csv.reader(f)
    header = next(reader)

    print("Running script ... ")
    for sid, name, attend in reader:
        db.execute("INSERT INTO attendance(sid, name, attend) VALUES(:i, :n, :a)", {"i": sid, "n": name, "a": attend})

    db.commit()
    
    print("Completed ... ")


if __name__ == "__main__":
    main()