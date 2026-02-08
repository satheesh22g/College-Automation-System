"""
Advanced Chatbot Module
Provides intelligent conversational interface with context-aware responses
Uses query handlers for role-based data retrieval
"""

from typing import Dict, Any, List
from autocorrect import Speller
from views.query_handlers import get_query_handler
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
import json

# Initialize blueprint
chatbot_bp = Blueprint('chatbot', __name__)

# Database will be set by app factory
db = None
spell = Speller(lang='en')


def init_chatbot(db_instance):
    """Initialize chatbot blueprint with database"""
    global db
    db = db_instance


class Chatbot:
    """
    Advanced chatbot for intelligent query processing
    Supports multiple user types with role-based responses
    """
    
    def __init__(self, db, user_id: str, user_type: str, user_name: str = None):
        """
        Initialize chatbot
        
        Args:
            db: Database session
            user_id: Current user's ID
            user_type: User type (Student, Faculty, HOD, etc.)
            user_name: User's display name
        """
        self.db = db
        self.user_id = user_id
        self.user_type = user_type
        self.user_name = user_name or user_id
        
        # Get appropriate handler for user type
        self.handler = get_query_handler(user_type, db, user_id)
        
        # Conversation history (for context)
        self.history = []
    
    def process_message(self, message: str) -> Dict[str, Any]:
        """
        Process user message and return intelligent response
        
        Args:
            message: User's natural language query
        
        Returns:
            {
                'success': bool,
                'response': str,
                'data': dict,
                'type': str,
                'suggestions': list
            }
        """
        try:
            # Clean and validate message
            message = message.strip()
            if not message:
                return self._empty_message_response()
            
            # Spell correct the message
            corrected_message = spell(message)
            
            # Add to history
            self.history.append({
                'role': 'user',
                'message': message,
                'timestamp': self._get_timestamp()
            })
            
            # Process with appropriate handler
            result = self.handler.handle(corrected_message)
            
            # Format response
            response = self._format_response(result)
            
            # Add to history
            self.history.append({
                'role': 'bot',
                'message': response['response'],
                'timestamp': self._get_timestamp()
            })
            
            return response
            
        except Exception as e:
            return self._error_response(str(e))
    
    def _format_response(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format handler result into conversational response
        
        Args:
            result: Result from query handler
        
        Returns:
            Formatted response with natural language message
        """
        if not result['success']:
            return {
                'success': False,
                'response': result['message'],
                'data': None,
                'type': result['type'],
                'suggestions': self._get_suggestions_for_user()
            }
        
        # Format data based on type
        formatted_message = self._format_data_message(result['type'], result['data'])
        
        return {
            'success': True,
            'response': formatted_message,
            'data': result['data'],
            'type': result['type'],
            'suggestions': self._get_suggestions_for_user()
        }
    
    def _format_data_message(self, data_type: str, data: Dict[str, Any]) -> str:
        """
        Format data into human-readable message based on type
        
        Args:
            data_type: Type of data returned
            data: The actual data
        
        Returns:
            Formatted message
        """
        if data_type == 'attendance':
            return (f"Your current attendance: {data.get('percentage', 0)}% "
                   f"({data.get('attendance', 0)} days) in Year {data.get('year', '?')}")
        
        elif data_type == 'marks':
            return (f"Your academic performance: Average {data.get('average', 0)}|%, "
                   f"Total: {data.get('total', 0)}, Subjects: {data.get('marks_count', 0)}")
        
        elif data_type == 'profile':
            data_obj = data
            return (f"✓ {data_obj.get('name', 'N/A')} ({data_obj.get('branch', 'N/A')}) "
                   f"- Year {data_obj.get('year', '?')}")
        
        elif data_type == 'subjects':
            return f"You have {data.get('count', 0)} subjects this semester"
        
        elif data_type == 'students_list':
            return f"You are guiding {data.get('count', 0)} students"
        
        elif data_type == 'attendance_list':
            return f"Attendance data for {data.get('count', 0)} students retrieved"
        
        elif data_type == 'marks_list':
            return f"Marks data for {data.get('count', 0)} students retrieved"
        
        elif data_type == 'count':
            return f"Total: {data.get('count', 0)} records found"
        
        elif data_type == 'failed_list':
            return f"⚠ {data.get('count', 0)} students need academic attention"
        
        elif data_type == 'low_attendance':
            return f"⚠ {data.get('count', 0)} students have attendance < 75%"
        
        elif data_type == 'dept_stats':
            return (f"Department Statistics:\n"
                   f"• Students: {data.get('total_students', 0)}\n"
                   f"• Marks Records: {data.get('total_marks', 0)}\n"
                   f"• Attendance Records: {data.get('total_attendance', 0)}")
        
        elif data_type == 'year_analysis':
            return (f"Year {data.get('year', '?')} Analysis:\n"
                   f"• Students: {data.get('students', 0)}\n"
                   f"• Marks Records: {data.get('marks', 0)}\n"
                   f"• Attendance: {data.get('attendance_records', 0)}")
        
        elif data_type == 'count_by_year':
            msg = "Student Distribution by Year:\n"
            for key, val in data.items():
                year = key.split('_')[1]
                msg += f"• Year {year}: {val} students\n"
            return msg
        
        elif data_type == 'dept_list':
            depts = data.get('departments', [])
            if not depts:
                return f"Total departments: {data.get('count', 0)}"
            msg = f"Departments ({data.get('count', 0)}):\n"
            for dept in depts:
                msg += f"• {dept.get('name', 'N/A')}\n"
            return msg
        
        elif data_type == 'user_list':
            users = data.get('users', [])
            if not users:
                return f"Total users: {data.get('count', 0)}"
            msg = f"System Users ({data.get('count', 0)}):\n"
            for user in users[:5]:  # Show first 5 users
                user_name = user.get('name') or user.get('username', 'N/A')
                msg += f"• {user.get('id', 'N/A')} - {user_name} ({user.get('type', 'N/A')})\n"
            if len(users) > 5:
                msg += f"• ... and {len(users) - 5} more\n"
            return msg
        
        elif data_type == 'system_status':
            return (f"System Status:\n"
                   f"• Students: {data.get('total_students', 0)}\n"
                   f"• Faculty: {data.get('total_faculty', 0)}\n"
                   f"• Users: {data.get('total_users', 0)}\n"
                   f"• Marks Records: {data.get('total_marks', 0)}\n"
                   f"• Attendance Records: {data.get('total_attendance', 0)}")
        
        elif data_type == 'help':
            return "Here's how to use this chatbot. Try the suggestions above!"
        
        elif data_type == 'features':
            return "This chatbot helps you query student and academic information based on your role in the system."
        
        else:
            # Handle cases where data is None or not a dict
            if data is None:
                return "✓ Query processed successfully"
            else:
                try:
                    return f"✓ Query processed: {len(data)} records found"
                except TypeError:
                    return "✓ Query processed successfully"
    
    def _get_suggestions_for_user(self) -> List[str]:
        """
        Get context-aware suggestions based on user type
        
        Returns:
            List of suggested queries
        """
        suggestions_map = {
            'Student': [
                "Show my attendance",
                "What are my marks?",
                "Tell me my profile",
                "What are my subjects?",
                "How much attendance do I need?"
            ],
            'Faculty': [
                "Show my students",
                "Student attendance status",
                "Who has low marks?",
                "Who has low attendance?",
                "Total count of my students"
            ],
            'counselor': [
                "Show my students",
                "Student attendance status",
                "Who has low marks?",
                "Who has low attendance?",
                "Total count of my students"
            ],
            'HOD': [
                "Department statistics",
                "Year 1 analysis",
                "Who failed?",
                "Attendance overview",
                "Count by year"
            ],
            'clerk': [
                "Show student statistics",
                "Total students count",
                "Department overview",
                "Failed students list",
                "Attendance summary"
            ],
            'admin': [
                "System statistics",
                "Total students",
                "Total faculty",
                "Department overview",
                "System status"
            ]
        }
        
        return suggestions_map.get(self.user_type, [
            "Ask about students",
            "Check attendance",
            "View marks",
            "Get statistics"
        ])
    
    def _empty_message_response(self) -> Dict[str, Any]:
        """Response for empty message"""
        return {
            'success': False,
            'response': f"Hi {self.user_name}! How can I help you today?",
            'data': None,
            'type': 'greeting',
            'suggestions': self._get_suggestions_for_user()
        }
    
    def _error_response(self, error: str) -> Dict[str, Any]:
        """Response for errors"""
        return {
            'success': False,
            'response': f"Sorry, an error occurred: {error}",
            'data': None,
            'type': 'error',
            'suggestions': self._get_suggestions_for_user()
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get conversation history summary"""
        return {
            'user': self.user_name,
            'user_type': self.user_type,
            'messages': len([m for m in self.history if m['role'] == 'user']),
            'responses': len([m for m in self.history if m['role'] == 'bot']),
            'history': self.history
        }


# ============================================
# CHATBOT ROUTES
# ============================================

@chatbot_bp.route("/chatbot")
def chatbot_page():
    """Chatbot interface page"""
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    from views.query import get_quick_queries
    
    user_type = session.get('usert', 'Student')
    quick_queries = get_quick_queries(user_type)
    
    return render_template('chatbot.html',
                          quick_queries=quick_queries,
                          username=session.get('namet', 'User'),
                          user_type=user_type)


@chatbot_bp.route("/api/chat", methods=["POST"])
def chat_api():
    """Chatbot API endpoint for processing queries"""
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
