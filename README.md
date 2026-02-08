# College Automation System

A modern, web-based college management system built with Flask and SQLAlchemy that streamlines academic operations including attendance tracking, marks management, student profiles, and feedback systems.

## About This System

The College Automation System is a comprehensive solution designed to automate and digitize college administrative processes. It provides role-based access for students, faculty members, heads of departments, counselors, and administrators with an intuitive, modern user interface.

### Key Features

- **Attendance Management**: Track and analyze student attendance with percentage calculations and automatic processing
- **Marks & Grades**: Manage and visualize academic marks with grading scales and performance analytics
- **Student Profiles**: Comprehensive student information management with personal and academic details
- **Feedback System**: Collect and manage feedback from students and faculty for continuous improvement
- **Natural Language Search**: Query academic data using conversational language patterns
- **Role-Based Access Control**: Different features and views based on user role (Student, Faculty, HOD, Counselor, Admin)
- **Data Import**: Import student data, attendance, and marks from Excel spreadsheets
- **Responsive Design**: Modern Bootstrap 5 interface that works on all devices

## User Roles & Permissions

### 1. **Students**
Students can:
- View their attendance records with percentage breakdown
- Check marks and academic performance
- Access their profile information
- Submit feedback and complaints
- Rate faculty members
- Search for academic information

### 2. **Faculty Members**
Faculty can:
- Query student data and attendance
- View student marks and profiles
- Receive and respond to feedback
- Submit suggestions and complaints

### 3. **Head of Department (HOD)**
HOD can:
- View department-wide attendance patterns
- Analyze marks and academic performance
- Manage student profiles
- Query data by academic year
- Monitor department feedback

### 4. **Counselor**
Counselors can:
- View counseling students' attendance
- Check marks of assigned students
- Manage student profiles
- Analyze attendance and performance trends

### 5. **Administrator/Clerk**
Administrators can:
- Import and load data from Excel files
- Manage system settings and configurations
- Reset user passwords
- Review all system feedback
- Manage departments and faculty profiles

## System Architecture

### Technology Stack
- **Backend**: Python 3.14.0 with Flask web framework
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5.3.0 with Font Awesome 6.4.0 icons
- **Session Management**: Flask-Session
- **Security**: Flask-Bcrypt for password hashing

### Database Tables
The system uses 10 primary tables:
- **Accounts**: User login credentials and authentication
- **Student_Profile**: Student personal and academic information
- **Attendance**: Attendance records with percentages
- **Marks**: Academic marks and grades
- **Faculty_Profile**: Faculty information and details
- **Faculty_Feedback**: Faculty ratings from students
- **Feedback**: General feedback and suggestions
- **Departments**: Department information
- **Faculty**: Faculty member data
- **Subjects**: Subject/course information

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- SQLite (included with Python)

### Installation Steps

1. **Clone the Repository**
```bash
git clone <repository-url>
cd College-Automation-System
```

2. **Create Virtual Environment** (Recommended)
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

3. **Install Required Packages**
```bash
pip install -r requirements.txt
```

4. **Initialize Database** (if needed)
```bash
python database.py
```

5. **Run the Application**
```bash
python app.py
```

6. **Access the System**
Open your web browser and navigate to:
```
http://localhost:5000
```

## Usage Guide

### For Students
1. **Login/Register**: Navigate to the home page and register or login with your credentials
2. **View Dashboard**: Access the main dashboard showing quick links to all features
3. **Check Attendance**: Click on "Attendance" to view your attendance records with visual percentage display
4. **View Marks**: Access the "Marks & Grades" section to see your academic performance
5. **Search Data**: Use the "Education Search Hub" to query your information
6. **Submit Feedback**: Go to "Feedback" to submit suggestions or rate faculty members

### For Faculty/HOD
1. **Use Education Search**: Search for student data by roll number or name
2. **View Performance**: Analyze attendance and marks data for students
3. **Submit Feedback**: Use the feedback system to provide suggestions

### For Administrators
1. **Load Data**: Go to "Load Data" to import student data from Excel files
2. **Reset Passwords**: Use "Password Reset" tool to reset user accounts
3. **View Feedback**: Check all submitted feedback from users

## Modern Design Features

All templates have been updated with:
- **Bootstrap 5**: Modern, responsive grid system
- **Color-Coded Data**: Attendance and marks shown with visual indicators
  - Green: Excellent (≥85% or A Grade)
  - Blue: Good (75-84% or B Grade)
  - Orange: Warning (65-74% or C Grade)
  - Red: Critical (<65% or D Grade)
- **Gradient Headers**: Visually appealing gradient backgrounds
- **Inline Help Text**: Each page includes helpful information about its purpose
- **Responsive Cards**: Touch-friendly interface for mobile devices
- **Easy Navigation**: Clear navigation menu and breadcrumbs
- **Empty States**: Helpful messages when no data is found
- **Form Validation**: Client and server-side validation

## Key Pages

### Public Pages
- **Home (intro.html)**: Welcome page with features overview and login link

### Student Pages
- **Dashboard (menu.html)**: Role-specific quick access cards
- **Attendance (attendance.html)**: Color-coded attendance with statistics
- **Marks (marks.html)**: Grade visualization with performance metrics
- **Feedback (feedback.html)**: Submit feedback and rate faculty
- **Help (help.html)**: FAQs and usage instructions

### Admin Pages
- **Load Data (load_data.html)**: Import data from Excel files
- **Password Reset (pswdreset.html)**: Reset user passwords

### Shared Pages
- **Login (login.html)**: Secure authentication with password toggle
- **Registration (registration.html)**: New user account creation
- **Search (query_set.html)**: Natural language data search
- **Feedback Summary (show_feedback.html)**: View faculty feedback

## Database Schema

### Attendance Table
- Roll No, Student ID, Name
- Attendance per subject (Sub1-13)
- Total attendance count and percentage
- Department, Year, Semester

### Marks Table
- Student ID, Name
- Marks per subject (Sub1-10)
- Total marks and average percentage
- Department, Year, Semester

### Student Profile Table
- SID, Name, Branch, Year
- Gender, Date of Birth, Entrance Type
- Department, Faculty Advisor

## API Endpoints

The system uses Flask routes for:
- `/` - Home page
- `/login` - User login
- `/register` - User registration
- `/dashboard` - Main dashboard
- `/query` - Search/query endpoint
- `/attendance` - Attendance records
- `/marks` - Marks and grades
- `/feedback` - Feedback submission
- `/help` - Help and FAQs

## Configuration

### Default Settings
- **Session Type**: Filesystem
- **Database**: SQLite (database.db)
- **Port**: 5000
- **Debug Mode**: Should be disabled in production

### Environment Variables
Update app.py for production use:
```python
app.debug = False  # Disable debug mode
app.secret_key = os.environ.get('SECRET_KEY')  # Use environment variable
```

## Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```bash
python app.py --port 5001
```

### Database Errors
If you encounter database errors:
```bash
# Delete existing database
rm database.db
# Reinitialize
python database.py
```

### Missing Dependencies
If you get import errors:
```bash
pip install --upgrade -r requirements.txt
```

## Security Considerations

- **Password Hashing**: All passwords are hashed using bcrypt
- **Session Management**: Flask-Session handles secure session management
- **Role-Based Access**: Routes check user role before displaying content
- **Input Validation**: All forms validate input on client and server side

## Performance Notes

- The system handles attendance data for multiple semesters
- Attendance calculations are optimized with percentage caching
- Search functionality uses pattern matching for flexible queries

## Future Enhancements

Potential improvements for future versions:
- Advanced analytics and reporting
- Email notifications for attendance/marks
- Mobile native applications
- Real-time notifications
- Integration with student information systems

## Support & Contact

For technical support or issues, please contact your college IT department.

## License

This project is developed for educational purposes at SRIT (Sri Ramanujan Institute of Technology).

## Author

Developed as a Batch B7 project for the College Automation System initiative.

---

**Last Updated**: 2024
**Version**: 2.0
**Status**: Production Ready
