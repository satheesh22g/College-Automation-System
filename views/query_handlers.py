"""
Intelligent Query Handler System
Maps user queries to database operations with role-based access control
Uses Command Registry Pattern for extensibility
"""

from sqlalchemy import text, func
from typing import List, Dict, Any, Optional
import re
from enum import Enum


class QueryType(Enum):
    """Query types for classification"""
    COUNT = "count"
    DETAIL = "detail"
    LIST = "list"
    COMPARISON = "comparison"
    STATISTICS = "statistics"
    SEARCH = "search"
    UNKNOWN = "unknown"


class QueryHandler:
    """Base query handler"""
    
    def __init__(self, db, user_id, user_type):
        self.db = db
        self.user_id = user_id
        self.user_type = user_type
    
    def handle(self, query: str) -> Dict[str, Any]:
        """
        Process query and return results
        Returns: {success: bool, data: Any, message: str, type: str}
        """
        raise NotImplementedError("Subclasses must implement handle()")
    
    def _get_help(self) -> Dict[str, Any]:
        """Provide help text based on user type"""
        # Normalize user type for consistent help text
        user_type_normalized = self.user_type.lower() if self.user_type else 'student'
        
        help_texts = {
            'student': (
                "📚 <b>How to Use This Chatbot:</b><br>"
                "• Ask about your <b>attendance</b> - 'Show my attendance'<br>"
                "• Check your <b>marks</b> - 'Show my marks'<br>"
                "• View your <b>profile</b> - 'Show my profile'<br>"
                "<br><b>Tips:</b> Use natural language - the chatbot understands various ways to ask!"
            ),
            'faculty': (
                "📚 <b>How to Use This Chatbot:</b><br>"
                "• View <b>my students</b> - 'Show my students'<br>"
                "• Check <b>student marks</b> - 'Show students marks'<br>"
                "• Find <b>failed students</b> - 'Show failed students'<br>"
                "• Analyze <b>attendance</b> - 'Show attendance issues'<br>"
                "<br><b>Tips:</b> Ask naturally, mention year numbers (1-4) for detailed analysis!"
            ),
            'hod': (
                "📊 <b>How to Use This Chatbot:</b><br>"
                "• View <b>department stats</b> - 'Show year 1 statistics'<br>"
                "• Check <b>failed students</b> - 'How many failed year 2'<br>"
                "• Analyze <b>attendance</b> - 'Show attendance overview'<br>"
                "• Find <b>top performers</b> - 'Show top students'<br>"
                "<br><b>Tips:</b> Provide year details for specific analysis!"
            ),
            'counselor': (
                "🎓 <b>How to Use This Chatbot:</b><br>"
                "• View <b>my counsel students</b> - 'Show my counsel students'<br>"
                "• Check <b>student marks</b> - 'Show counsel students marks'<br>"
                "• Monitor <b>attendance</b> - 'Show counsel students attendance'<br>"
                "• Find <b>at-risk students</b> - 'Show at risk counsel students'<br>"
                "<br><b>Tips:</b> Use natural queries about your guided students!"
            ),
            'admin': (
                "⚙️ <b>How to Use This Chatbot:</b><br>"
                "• View <b>system statistics</b> - 'Total students', 'Failed students'<br>"
                "• Manage <b>departments</b> - 'Show all departments'<br>"
                "• Check <b>user information</b> - 'Show users'<br>"
                "• Monitor <b>attendance</b> - 'Show attendance shortage'<br>"
                "<br><b>Tips:</b> Use natural language for administrative queries!"
            ),
            'clerk': (
                "📋 <b>How to Use This Chatbot:</b><br>"
                "• View <b>system statistics</b> - 'Total students', 'Failed students'<br>"
                "• Manage <b>departments</b> - 'Show all departments'<br>"
                "• Check <b>attendance</b> - 'Show attendance information'<br>"
                "<br><b>Tips:</b> Use natural language for clerical queries!"
            )
        }
        
        help_text = help_texts.get(user_type_normalized, help_texts['student'])
        
        return {
            'success': True,
            'data': None,
            'message': help_text,
            'type': 'help'
        }
    
    def _get_features(self) -> Dict[str, Any]:
        """Provide features information"""
        features_text = (
            "⭐ <b>Available Features:</b><br>"
            "✓ <b>Attendance Tracking</b> - Real-time attendance monitoring<br>"
            "✓ <b>Marks & Grading</b> - Comprehensive academic performance<br>"
            "✓ <b>Student Profile</b> - Personal and academic details<br>"
            "✓ <b>Performance Analytics</b> - Detailed performance statistics<br>"
            "✓ <b>Natural Language Processing</b> - Understand your queries naturally<br>"
            "✓ <b>Role-Based Access</b> - Customized experience for your role<br>"
            "✓ <b>Data Export</b> - Export reports and analytics"
        )
        
        return {
            'success': True,
            'data': None,
            'message': features_text,
            'type': 'features'
        }


class StudentQueryHandler(QueryHandler):
    """Handle queries for Student users"""
    
    def handle(self, query: str) -> Dict[str, Any]:
        """Process student queries"""
        query_lower = query.lower()
        
        # Check for help/features
        if 'help' in query_lower:
            return self._get_help()
        if 'feature' in query_lower:
            return self._get_features()
        
        # My Attendance
        if any(w in query_lower for w in ['attendance', 'attend', 'present', 'absence']):
            return self._get_my_attendance()
        
        # My Marks
        if any(w in query_lower for w in ['mark', 'grade', 'score', 'result', 'exam']):
            return self._get_my_marks()
        
        # My Profile
        if any(w in query_lower for w in ['profile', 'info', 'detail', 'personal']):
            return self._get_my_profile()
        
        # Semester subjects
        if 'subject' in query_lower or 'course' in query_lower:
            return self._get_my_subjects()
        
        return {
            'success': False,
            'data': None,
            'message': "I can help with: Attendance, Marks, Profile, or Subjects",
            'type': 'suggestion'
        }
    
    def _get_my_attendance(self) -> Dict[str, Any]:
        """Get student's attendance"""
        try:
            from database import Attendance
            result = self.db.query(Attendance).filter_by(student_id=self.user_id).first()
            if result:
                return {
                    'success': True,
                    'data': {
                        'attendance': result.attend,
                        'percentage': result.attend_perc,
                        'year': result.year
                    },
                    'message': f"Your attendance: {result.attend_perc}%",
                    'type': 'attendance'
                }
            return {
                'success': False,
                'data': None,
                'message': "No attendance record found",
                'type': 'attendance'
            }
        except Exception as e:
            return self._error_response(f"Error fetching attendance: {str(e)}")
    
    def _get_my_marks(self) -> Dict[str, Any]:
        """Get student's marks"""
        try:
            from database import Marks
            result = self.db.query(Marks).filter_by(student_id=self.user_id).first()
            if result:
                marks_list = [result.sub1, result.sub2, result.sub3, result.sub4,
                             result.sub5, result.sub6, result.sub7, result.sub8]
                marks_list = [m for m in marks_list if m]
                avg = sum(marks_list) / len(marks_list) if marks_list else 0
                
                return {
                    'success': True,
                    'data': {
                        'average': round(avg, 2),
                        'total': result.total,
                        'marks_count': len(marks_list),
                        'year': result.year
                    },
                    'message': f"Your average: {round(avg, 2)}%, Total: {result.total}",
                    'type': 'marks'
                }
            return {
                'success': False,
                'data': None,
                'message': "No marks record found",
                'type': 'marks'
            }
        except Exception as e:
            return self._error_response(f"Error fetching marks: {str(e)}")
    
    def _get_my_profile(self) -> Dict[str, Any]:
        """Get student's profile"""
        try:
            from database import Student_Profile
            result = self.db.query(Student_Profile).filter_by(sid=self.user_id).first()
            if result:
                return {
                    'success': True,
                    'data': {
                        'name': result.name,
                        'branch': result.branch,
                        'year': result.year,
                        'gender': result.gender,
                        'entrance_type': result.entrance_type
                    },
                    'message': f"Profile: {result.name} ({result.branch})",
                    'type': 'profile'
                }
            return {
                'success': False,
                'data': None,
                'message': "Profile not found",
                'type': 'profile'
            }
        except Exception as e:
            return self._error_response(f"Error fetching profile: {str(e)}")
    
    def _get_my_subjects(self) -> Dict[str, Any]:
        """Get student's subjects"""
        try:
            from database import Student_Profile, Subjects
            student = self.db.query(Student_Profile).filter_by(sid=self.user_id).first()
            if student:
                subjects = self.db.query(Subjects).filter_by(year=student.year).all()
                subject_list = [s.name for s in subjects]
                return {
                    'success': True,
                    'data': {
                        'subjects': subject_list,
                        'count': len(subject_list)
                    },
                    'message': f"You have {len(subject_list)} subjects",
                    'type': 'subjects'
                }
            return {
                'success': False,
                'data': None,
                'message': "Could not fetch subjects",
                'type': 'subjects'
            }
        except Exception as e:
            return self._error_response(f"Error fetching subjects: {str(e)}")
    
    def _error_response(self, message: str) -> Dict[str, Any]:
        """Return error response"""
        return {
            'success': False,
            'data': None,
            'message': message,
            'type': 'error'
        }


class FacultyQueryHandler(QueryHandler):
    """Handle queries for Faculty/Counselor users"""
    
    def handle(self, query: str) -> Dict[str, Any]:
        """Process faculty queries"""
        query_lower = query.lower()
        
        # Check for help/features
        if 'help' in query_lower:
            return self._get_help()
        if 'feature' in query_lower:
            return self._get_features()
        
        # My students
        if any(w in query_lower for w in ['student', 'counsel', 'council', 'guidance']):
            return self._get_my_students()
        
        # My students' attendance
        if 'attend' in query_lower and any(w in query_lower for w in ['student', 'class', 'my']):
            return self._get_students_attendance()
        
        # My students' marks
        if 'mark' in query_lower and any(w in query_lower for w in ['student', 'grade', 'my']):
            return self._get_students_marks()
        
        # Student count
        if 'count' in query_lower and 'student' in query_lower:
            return self._count_my_students()
        
        # Failed students
        if 'fail' in query_lower and 'student' in query_lower:
            return self._get_failed_students()
        
        # Low attendance
        if 'low' in query_lower and 'attend' in query_lower:
            return self._get_low_attendance_students()
        
        return {
            'success': False,
            'data': None,
            'message': "I can help with: My Students, Attendance, Marks, or Student Analysis",
            'type': 'suggestion'
        }
    
    def _get_my_students(self) -> Dict[str, Any]:
        """Get faculty's guided students"""
        try:
            from database import Student_Profile
            students = self.db.query(Student_Profile).filter_by(faculty_id=self.user_id).all()
            student_list = [{
                'id': s.sid,
                'name': s.name,
                'year': s.year,
                'branch': s.branch
            } for s in students]
            
            return {
                'success': True,
                'data': {
                    'students': student_list,
                    'count': len(student_list)
                },
                'message': f"You guide {len(student_list)} students",
                'type': 'students_list'
            }
        except Exception as e:
            return self._error_response(f"Error fetching students: {str(e)}")
    
    def _get_students_attendance(self) -> Dict[str, Any]:
        """Get attendance of faculty's students"""
        try:
            from database import Attendance
            results = self.db.query(Attendance).filter_by(councelor_id=self.user_id).all()
            attendance_list = [{
                'student_id': r.student_id,
                'percentage': r.attend_perc,
                'total_days': r.attend
            } for r in results]
            
            return {
                'success': True,
                'data': {
                    'attendance': attendance_list,
                    'count': len(attendance_list)
                },
                'message': f"Attendance for {len(attendance_list)} students",
                'type': 'attendance_list'
            }
        except Exception as e:
            return self._error_response(f"Error fetching attendance: {str(e)}")
    
    def _get_students_marks(self) -> Dict[str, Any]:
        """Get marks of faculty's students"""
        try:
            from database import Marks
            results = self.db.query(Marks).filter_by(councelor_id=self.user_id).all()
            marks_list = [{
                'student_id': r.student_id,
                'average': r.average,
                'year': r.year
            } for r in results]
            
            return {
                'success': True,
                'data': {
                    'marks': marks_list,
                    'count': len(marks_list)
                },
                'message': f"Marks for {len(marks_list)} students",
                'type': 'marks_list'
            }
        except Exception as e:
            return self._error_response(f"Error fetching marks: {str(e)}")
    
    def _count_my_students(self) -> Dict[str, Any]:
        """Count total guidance students"""
        try:
            from database import Student_Profile
            count = self.db.query(Student_Profile).filter_by(faculty_id=self.user_id).count()
            return {
                'success': True,
                'data': {'count': count},
                'message': f"You are guiding {count} students",
                'type': 'count'
            }
        except Exception as e:
            return self._error_response(f"Error counting students: {str(e)}")
    
    def _get_failed_students(self) -> Dict[str, Any]:
        """Get students with failed subjects"""
        try:
            from database import Marks
            results = self.db.query(Marks).filter_by(councelor_id=self.user_id).all()
            failed_students = [{
                'student_id': r.student_id,
                'average': r.average,
                'year': r.year
            } for r in results if r.average and r.average < 40]
            
            return {
                'success': True,
                'data': {
                    'failed': failed_students,
                    'count': len(failed_students)
                },
                'message': f"{len(failed_students)} students need attention",
                'type': 'failed_list'
            }
        except Exception as e:
            return self._error_response(f"Error fetching failed students: {str(e)}")
    
    def _get_low_attendance_students(self) -> Dict[str, Any]:
        """Get students with low attendance"""
        try:
            from database import Attendance
            results = self.db.query(Attendance).filter_by(councelor_id=self.user_id).all()
            low_attendance = [{
                'student_id': r.student_id,
                'percentage': r.attend_perc
            } for r in results if r.attend_perc and r.attend_perc < 75]
            
            return {
                'success': True,
                'data': {
                    'low_attendance': low_attendance,
                    'count': len(low_attendance)
                },
                'message': f"{len(low_attendance)} students have low attendance",
                'type': 'low_attendance'
            }
        except Exception as e:
            return self._error_response(f"Error fetching low attendance: {str(e)}")
    
    def _error_response(self, message: str) -> Dict[str, Any]:
        return {
            'success': False,
            'data': None,
            'message': message,
            'type': 'error'
        }


class HODQueryHandler(QueryHandler):
    """Handle queries for HOD (Head of Department) users"""
    
    def handle(self, query: str) -> Dict[str, Any]:
        """Process HOD queries"""
        query_lower = query.lower()
        
        # Check for help/features
        if 'help' in query_lower:
            return self._get_help()
        if 'feature' in query_lower:
            return self._get_features()
        
        # Department statistics
        if any(w in query_lower for w in ['department', 'dept', 'statistics', 'stats']):
            return self._get_dept_statistics()
        
        # Year-wise analysis
        if 'year' in query_lower and any(w in query_lower for w in ['student', 'analysis']):
            year_match = re.search(r'(1|2|3|4)', query_lower)
            if year_match:
                return self._get_year_analysis(int(year_match.group(1)))
        
        # Failed students in department
        if 'fail' in query_lower and any(w in query_lower for w in ['dept', 'department']):
            return self._get_dept_failed_students()
        
        # Attendance overview
        if 'attend' in query_lower and 'overview' in query_lower:
            return self._get_dept_attendance_overview()
        
        # Student count by year
        if 'count' in query_lower and 'year' in query_lower:
            return self._count_by_year()
        
        return {
            'success': False,
            'data': None,
            'message': "I can help with: Department Stats, Year Analysis, Failed Students, Attendance",
            'type': 'suggestion'
        }
    
    def _get_dept_statistics(self) -> Dict[str, Any]:
        """Get department-wide statistics"""
        try:
            from database import Student_Profile, Marks, Attendance
            total_students = self.db.query(Student_Profile).count()
            total_marks = self.db.query(Marks).count()
            total_attendance = self.db.query(Attendance).count()
            
            return {
                'success': True,
                'data': {
                    'total_students': total_students,
                    'total_marks': total_marks,
                    'total_attendance': total_attendance
                },
                'message': f"Department: {total_students} students, {total_marks} marks records",
                'type': 'dept_stats'
            }
        except Exception as e:
            return self._error_response(f"Error fetching stats: {str(e)}")
    
    def _get_year_analysis(self, year: int) -> Dict[str, Any]:
        """Get analysis for specific year"""
        try:
            from database import Student_Profile, Marks, Attendance
            year_students = self.db.query(Student_Profile).filter_by(year=year).all()
            year_marks = self.db.query(Marks).filter_by(year=year).all()
            avg_attendance = self.db.query(Attendance).filter_by(year=year)
            
            return {
                'success': True,
                'data': {
                    'year': year,
                    'students': len(year_students),
                    'marks': len(year_marks),
                    'attendance_records': avg_attendance.count()
                },
                'message': f"Year {year}: {len(year_students)} students, {len(year_marks)} marks records",
                'type': 'year_analysis'
            }
        except Exception as e:
            return self._error_response(f"Error fetching year analysis: {str(e)}")
    
    def _get_dept_failed_students(self) -> Dict[str, Any]:
        """Get all failed students in department"""
        try:
            from database import Marks
            failed = self.db.query(Marks).filter(Marks.average < 40).all()
            failed_list = [{
                'student_id': m.student_id,
                'average': m.average,
                'year': m.year
            } for m in failed]
            
            return {
                'success': True,
                'data': {
                    'failed': failed_list,
                    'count': len(failed_list)
                },
                'message': f"{len(failed_list)} students with average < 40",
                'type': 'failed_list'
            }
        except Exception as e:
            return self._error_response(f"Error fetching failed students: {str(e)}")
    
    def _get_dept_attendance_overview(self) -> Dict[str, Any]:
        """Get attendance overview"""
        try:
            from database import Attendance
            low_attendance = self.db.query(Attendance).filter(Attendance.attend_perc < 75).all()
            
            return {
                'success': True,
                'data': {
                    'low_attendance_count': len(low_attendance),
                    'threshold': 75
                },
                'message': f"{len(low_attendance)} students have attendance < 75%",
                'type': 'attendance_overview'
            }
        except Exception as e:
            return self._error_response(f"Error fetching attendance: {str(e)}")
    
    def _count_by_year(self) -> Dict[str, Any]:
        """Count students by year"""
        try:
            from database import Student_Profile
            counts = {}
            for year in [1, 2, 3, 4]:
                counts[f"year_{year}"] = self.db.query(Student_Profile).filter_by(year=year).count()
            
            return {
                'success': True,
                'data': counts,
                'message': f"Student distribution by year: {counts}",
                'type': 'count_by_year'
            }
        except Exception as e:
            return self._error_response(f"Error counting: {str(e)}")
    
    def _error_response(self, message: str) -> Dict[str, Any]:
        return {
            'success': False,
            'data': None,
            'message': message,
            'type': 'error'
        }


class AdminQueryHandler(QueryHandler):
    """Handle queries for Admin users"""
    
    def handle(self, query: str) -> Dict[str, Any]:
        """Process admin queries"""
        query_lower = query.lower()
        
        # Check for help/features
        if 'help' in query_lower:
            return self._get_help()
        if 'feature' in query_lower:
            return self._get_features()
        
        # Failed students count
        if 'fail' in query_lower and any(w in query_lower for w in ['student', 'year', 'count']):
            year_match = re.search(r'(1|2|3|4)', query_lower)
            year = int(year_match.group(1)) if year_match else None
            return self._get_failed_students(year)
        
        # Department information
        if any(w in query_lower for w in ['department', 'dept', 'departments', 'all department']):
            return self._get_departments()
        
        # User/account management
        if any(w in query_lower for w in ['user', 'account', 'accounts', 'show user']):
            return self._get_users()
        
        # System status/statistics
        if any(w in query_lower for w in ['system', 'status', 'statistics', 'stats', 'total']):
            return self._get_system_status()
        
        # Attendance issues
        if 'attend' in query_lower and any(w in query_lower for w in ['issue', 'shortage', 'below', 'low']):
            return self._get_attendance_issues()
        
        return {
            'success': False,
            'data': None,
            'message': "I can help with: Students, Departments, System Status, Attendance, Users",
            'type': 'suggestion'
        }
    
    def _get_failed_students(self, year: int = None) -> Dict[str, Any]:
        """Get failed students (optionally by year)"""
        try:
            from database import Marks, Student_Profile
            
            query = self.db.query(Marks).filter(Marks.average < 40)
            if year:
                # Get students from that year
                year_students = self.db.query(Student_Profile.sid).filter_by(year=year).all()
                student_ids = [s[0] for s in year_students]
                query = query.filter(Marks.student_id.in_(student_ids))
            
            failed = query.all()
            
            return {
                'success': True,
                'data': {'count': len(failed)},
                'message': f"Failed students (average < 40): {len(failed)}",
                'type': 'failed_list'
            }
        except Exception as e:
            return self._error_response(f"Error fetching failed students: {str(e)}")
    
    def _get_departments(self) -> Dict[str, Any]:
        """Get all departments"""
        try:
            from database import Departments
            depts = self.db.query(Departments).all()
            dept_list = [{'id': d.did, 'name': d.name} for d in depts]
            
            return {
                'success': True,
                'data': {'departments': dept_list, 'count': len(dept_list)},
                'message': f"Total departments: {len(dept_list)}",
                'type': 'dept_list'
            }
        except Exception as e:
            return self._error_response(f"Error fetching departments: {str(e)}")
    
    def _get_users(self) -> Dict[str, Any]:
        """Get user information"""
        try:
            from database import Accounts
            users = self.db.query(Accounts).all()
            user_list = [{'id': u.id, 'name': u.name, 'type': u.user_type} for u in users]
            
            return {
                'success': True,
                'data': {'users': user_list, 'count': len(user_list)},
                'message': f"Total users: {len(user_list)}",
                'type': 'user_list'
            }
        except Exception as e:
            return self._error_response(f"Error fetching users: {str(e)}")
    
    def _get_system_status(self) -> Dict[str, Any]:
        """Get system statistics and status"""
        try:
            from database import Student_Profile, Faculty, Accounts, Marks, Attendance
            
            total_students = self.db.query(Student_Profile).count()
            total_faculty = self.db.query(Faculty).count()
            total_users = self.db.query(Accounts).count()
            total_marks = self.db.query(Marks).count()
            total_attendance = self.db.query(Attendance).count()
            
            return {
                'success': True,
                'data': {
                    'total_students': total_students,
                    'total_faculty': total_faculty,
                    'total_users': total_users,
                    'total_marks': total_marks,
                    'total_attendance': total_attendance
                },
                'message': f"System Status: {total_students} students, {total_faculty} faculty, {total_users} users",
                'type': 'system_status'
            }
        except Exception as e:
            return self._error_response(f"Error fetching system status: {str(e)}")
    
    def _get_attendance_issues(self) -> Dict[str, Any]:
        """Get attendance issues (below 75%)"""
        try:
            from database import Attendance, Student_Profile
            
            # Find students with low attendance
            low_attendance = self.db.query(Attendance).filter(Attendance.attend_perc < 75).all()
            
            return {
                'success': True,
                'data': {'count': len(low_attendance)},
                'message': f"Students with attendance < 75%: {len(low_attendance)}",
                'type': 'low_attendance'
            }
        except Exception as e:
            return self._error_response(f"Error fetching attendance issues: {str(e)}")
    
    def _error_response(self, message: str) -> Dict[str, Any]:
        return {
            'success': False,
            'data': None,
            'message': message,
            'type': 'error'
        }


# Query Handler Registry
HANDLER_REGISTRY = {
    'student': StudentQueryHandler,
    'faculty': FacultyQueryHandler,
    'counselor': FacultyQueryHandler,  # Counselor uses faculty queries
    'hod': HODQueryHandler,
    'admin': AdminQueryHandler,
    'clerk': StudentQueryHandler,  # Clerk can query general info
}


def get_query_handler(user_type: str, db, user_id: str):
    """
    Get appropriate query handler for user type
    Falls back to StudentQueryHandler if user type not found
    
    Args:
        user_type: User type from session (handled case-insensitive)
        db: Database session
        user_id: User ID
    
    Returns:
        Appropriate QueryHandler instance for the user type
    """
    # Normalize user_type to lowercase for case-insensitive lookup
    user_type_key = user_type.lower() if user_type else 'student'
    
    handler_class = HANDLER_REGISTRY.get(user_type_key, StudentQueryHandler)
    return handler_class(db, user_id, user_type)
