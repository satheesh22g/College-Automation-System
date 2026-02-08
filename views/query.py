"""
Query processing and intelligent search blueprint
Handles NLP-based query processing for student data
Uses advanced Chatbot for conversational interface
"""

from flask import Blueprint, render_template, request, session, redirect, url_for, flash, jsonify
from views.chatbot import Chatbot
from views.query_handlers import get_query_handler

# Initialize blueprint
query_bp = Blueprint('query', __name__)

# Will be set by app factory
db = None


def init_query(db_instance):
    """Initialize query blueprint with database"""
    global db
    db = db_instance


def get_quick_queries(user_type):
    """
    Generate dynamic quick queries based on user type
    Returns a list of query categories with items
    """
    # Normalize user type to handle case variations
    user_type_check = user_type.lower() if user_type else "student"
    
    if user_type_check == "student":
        return [
            {
                "title": "Student Info",
                "icon": "fas fa-graduation-cap",
                "items": [
                    {"text": "My Attendance", "icon": "fas fa-clipboard-list", "query": "Show my attendance"},
                    {"text": "My Marks", "icon": "fas fa-chart-bar", "query": "Show my marks"},
                    {"text": "My Profile", "icon": "fas fa-id-card", "query": "Show my profile"}
                ]
            },
            {
                "title": "Help",
                "icon": "fas fa-question-circle",
                "items": [
                    {"text": "How to Use", "icon": "fas fa-info-circle", "query": "Help"},
                    {"text": "Features", "icon": "fas fa-star", "query": "Features"}
                ]
            }
        ]
    
    elif user_type_check == "faculty":
        return [
            {
                "title": "Faculty Queries",
                "icon": "fas fa-chalkboard-user",
                "items": [
                    {"text": "My Students", "icon": "fas fa-users", "query": "Show my students"},
                    {"text": "Students Marks", "icon": "fas fa-chart-bar", "query": "Show students marks"},
                    {"text": "Failed Students", "icon": "fas fa-search", "query": "Show failed students"}
                ]
            },
            {
                "title": "Analysis",
                "icon": "fas fa-bar-chart",
                "items": [
                    {"text": "Attendance Issues", "icon": "fas fa-exclamation-triangle", "query": "Show attendance below 75%"},
                    {"text": "Performance Stats", "icon": "fas fa-chart-line", "query": "Show class performance"}
                ]
            },
            {
                "title": "Help",
                "icon": "fas fa-question-circle",
                "items": [
                    {"text": "How to Use", "icon": "fas fa-info-circle", "query": "Help"},
                    {"text": "Features", "icon": "fas fa-star", "query": "Features"}
                ]
            }
        ]
    
    elif user_type_check == "hod":
        return [
            {
                "title": "Department Analytics",
                "icon": "fas fa-building",
                "items": [
                    {"text": "Year 1 Analysis", "icon": "fas fa-bar-chart", "query": "Show year 1 statistics"},
                    {"text": "Year 2 Analysis", "icon": "fas fa-bar-chart", "query": "Show year 2 statistics"},
                    {"text": "Year 3 Analysis", "icon": "fas fa-bar-chart", "query": "Show year 3 statistics"}
                ]
            },
            {
                "title": "Performance",
                "icon": "fas fa-chart-line",
                "items": [
                    {"text": "Failed Students", "icon": "fas fa-search", "query": "How many failed year 1"},
                    {"text": "Attendance Overview", "icon": "fas fa-clipboard-list", "query": "Show attendance overview"},
                    {"text": "Top Performers", "icon": "fas fa-trophy", "query": "Show top students"}
                ]
            },
            {
                "title": "Help",
                "icon": "fas fa-question-circle",
                "items": [
                    {"text": "How to Use", "icon": "fas fa-info-circle", "query": "Help"},
                    {"text": "Features", "icon": "fas fa-star", "query": "Features"}
                ]
            }
        ]
    
    elif user_type_check == "counselor":
        return [
            {
                "title": "Counselor",
                "icon": "fas fa-user-tie",
                "items": [
                    {"text": "My Counsel Students", "icon": "fas fa-users", "query": "Show my counsel students"},
                    {"text": "Students Marks", "icon": "fas fa-book", "query": "Show counsel students marks"},
                    {"text": "Attendance Status", "icon": "fas fa-clipboard-list", "query": "Show counsel students attendance"}
                ]
            },
            {
                "title": "Analysis",
                "icon": "fas fa-bar-chart",
                "items": [
                    {"text": "At Risk Students", "icon": "fas fa-exclamation-circle", "query": "Show at risk counsel students"},
                    {"text": "Performance", "icon": "fas fa-chart-bar", "query": "Show counsel students performance"}
                ]
            },
            {
                "title": "Help",
                "icon": "fas fa-question-circle",
                "items": [
                    {"text": "How to Use", "icon": "fas fa-info-circle", "query": "Help"},
                    {"text": "Features", "icon": "fas fa-star", "query": "Features"}
                ]
            }
        ]
    
    else:  # Admin, Clerk, or other roles
        return [
            {
                "title": "Admin Queries",
                "icon": "fas fa-users",
                "items": [
                    {"text": "Total Students", "icon": "fas fa-users", "query": "How many students"},
                    {"text": "Failed Students", "icon": "fas fa-search", "query": "How many students failed in year 1"},
                    {"text": "Attendance Issues", "icon": "fas fa-exclamation-triangle", "query": "Show attendance shortage in year 2"}
                ]
            },
            {
                "title": "System",
                "icon": "fas fa-cog",
                "items": [
                    {"text": "Departments", "icon": "fas fa-building", "query": "Show all departments"},
                    {"text": "User Management", "icon": "fas fa-user-cog", "query": "Show users"},
                    {"text": "System Status", "icon": "fas fa-heartbeat", "query": "System status"}
                ]
            },
            {
                "title": "Help",
                "icon": "fas fa-question-circle",
                "items": [
                    {"text": "How to Use", "icon": "fas fa-info-circle", "query": "Help"},
                    {"text": "Features", "icon": "fas fa-star", "query": "Features"}
                ]
            }
        ]


def generate_query_suggestions(query, user_role="Student"):
    """
    Generate intelligent query suggestions based on input keywords
    Provides helpful hints for unrecognized queries
    """
    query_lower = query.lower()
    suggestions = []
    
    # Keyword mapping for intelligent suggestions
    if user_role == "Student":
        if any(word in query_lower for word in ['attend', 'present', 'absence', 'days', 'percent']):
            suggestions.append("'show my attendance' - View your attendance records")
        if any(word in query_lower for word in ['mark', 'grade', 'score', 'result', 'test', 'exam']):
            suggestions.append("'show my marks' - Check your academic marks")
        if any(word in query_lower for word in ['profile', 'info', 'detail', 'personal', 'about']):
            suggestions.append("'my profile' - View your personal information")
    else:
        if any(word in query_lower for word in ['attend', 'present', 'absence']):
            suggestions.append("Try: 'attendance', 'less than 75', 'shortage'")
        if any(word in query_lower for word in ['mark', 'grade', 'score']):
            suggestions.append("Try: 'compare graph marks year 2' or search by roll")
        if any(word in query_lower for word in ['profile', 'student', 'search']):
            suggestions.append("Try: Roll number (e.g., '161CS027') or student name")
        if any(word in query_lower for word in ['fail', 'failed']):
            suggestions.append("Try: 'how many fail year 2' with year 1-4")
        if any(word in query_lower for word in ['counsel', 'council']):
            suggestions.append("Try: 'show counsel students' for your guided students")
    
    # Return default suggestions if no matches
    if not suggestions:
        if user_role == "Student":
            suggestions = [
                "'show my attendance' - View attendance",
                "'show my marks' - Check marks",
                "'my profile' - View your info"
            ]
        else:
            suggestions = [
                "Enter roll number (e.g., '161CS027')",
                "Search by student name",
                "Use 'attendance', 'marks' for queries"
            ]
    
    return suggestions


@query_bp.route("/chatbot")
def chatbot_page():
    """
    Chatbot interface page
    Provides conversational UI for queries
    """
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    user_type = session.get('usert', 'Student')
    quick_queries = get_quick_queries(user_type)
    
    return render_template('chatbot.html', 
                          username=session.get('namet', 'User'),
                          user_type=user_type,
                          quick_queries=quick_queries)


@query_bp.route("/api/chat", methods=["POST"])
def chat_api():
    """
    ChatBot API endpoint
    Processes natural language queries and returns JSON response
    Supports all user types (Student, Faculty, HOD, Clerk, Admin)
    
    Query Examples:
    - Student: "show my attendance", "what are my marks", "my profile"
    - Faculty: "show my students", "who has low attendance", "failed students"
    - HOD: "department statistics", "year 2 analysis", "attendance overview"
    - Clerk: "total students", "department overview", "system status"
    """
    if 'user' not in session:
        return jsonify({
            'success': False,
            'response': 'Please login first',
            'type': 'error'
        }), 401
    
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'success': False,
                'response': 'Please enter a message',
                'type': 'empty'
            })
        
        # Initialize chatbot with user context
        chatbot = Chatbot(
            db=db,
            user_id=session.get('user'),
            user_type=session.get('usert', 'Student'),
            user_name=session.get('namet', 'User')
        )
        
        # Process message through intelligent chatbot
        result = chatbot.process_message(user_message)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'response': f'Error processing query: {str(e)}',
            'type': 'error'
        })


@query_bp.route("/query", methods=["GET", "POST"])
def query_set():
    """
    Legacy query interface (for backward compatibility)
    Processes queries via traditional form submission
    Uses intelligent chatbot backend for consistent results
    """
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    flash(session['namet'], "name")
    
    if request.method == 'GET':
        return render_template('query_set.html', suggestions=None)
    
    try:
        user_query = request.form.get("query", "").lower().strip()
        
        if not user_query:
            flash("Please enter a query", "error")
            return redirect(url_for('query.query_set'))
        
        # Initialize chatbot with user context
        chatbot = Chatbot(
            db=db,
            user_id=session.get('user'),
            user_type=session.get('usert', 'Student'),
            user_name=session.get('namet', 'User')
        )
        
        # Process message through intelligent chatbot
        result = chatbot.process_message(user_query)
        
        if result['success']:
            flash(f"✓ {result['response']}", "alert")
            
            # Return data in structured format
            return render_template('query_result.html',
                                  query=user_query,
                                  result=result)
        else:
            # No direct match - show suggestions
            suggestions = result['suggestions']
            return render_template('query_set.html', 
                                  suggestions=suggestions,
                                  user_query=user_query)
        
    except ValueError as e:
        flash("Invalid input format", "error")
        return redirect(url_for('query.query_set'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('query.query_set'))
