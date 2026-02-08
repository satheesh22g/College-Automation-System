"""
Performance Optimization Utilities
Helps improve database query performance and application speed
"""

import time
from functools import wraps
from flask import g
from sqlalchemy.orm import joinedload
from database import db

# Query Caching Decorator
def cache_query(timeout=300):
    """
    Cache query results for a specified time period
    Usage: @cache_query(timeout=600)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = f"{f.__name__}_{str(args)}_{str(kwargs)}"
            
            if cache_key in g:
                return g.cache[cache_key]
            
            result = f(*args, **kwargs)
            
            if not hasattr(g, 'cache'):
                g.cache = {}
            
            g.cache[cache_key] = result
            return result
        return decorated_function
    return decorator

# Query Performance Monitor
class QueryMonitor:
    def __init__(self):
        self.queries = []
        self.total_time = 0

    def log_query(self, query_text, execution_time):
        """Log a database query and its execution time"""
        self.queries.append({
            'query': query_text,
            'time': execution_time
        })
        self.total_time += execution_time

    def get_report(self):
        """Generate a performance report"""
        if not self.queries:
            return "No queries logged"
        
        slow_queries = [q for q in self.queries if q['time'] > 0.1]
        return {
            'total_queries': len(self.queries),
            'total_time': round(self.total_time, 4),
            'slow_queries': len(slow_queries),
            'average_time': round(self.total_time / len(self.queries), 4) if self.queries else 0
        }

# Database Query Optimization Helpers
class QueryOptimizer:
    """Provides optimized query patterns"""
    
    @staticmethod
    def get_student_with_relations(student_id):
        """Get student with all related data in one optimized query"""
        from database import Student_Profile, Attendance, Marks
        
        return db.query(Student_Profile).options(
            joinedload('attendance'),
            joinedload('marks'),
            joinedload('departments')
        ).filter_by(sid=student_id).first()
    
    @staticmethod
    def get_attendance_stats(student_id):
        """Get attendance statistics efficiently"""
        from database import Attendance
        from sqlalchemy import func, and_
        
        return db.query(
            func.sum(Attendance.attend).label('total_attend'),
            func.count(Attendance.sid).label('total_sessions'),
            func.avg(Attendance.attend_perc).label('avg_attendance')
        ).filter(Attendance.student_id == student_id).first()
    
    @staticmethod
    def get_marks_stats(student_id):
        """Get marks statistics efficiently"""
        from database import Marks
        from sqlalchemy import func
        
        return db.query(
            func.avg(Marks.average).label('avg_marks'),
            func.max(Marks.average).label('max_marks'),
            func.min(Marks.average).label('min_marks'),
            func.count(Marks.id).label('total_semesters')
        ).filter(Marks.student_id == student_id).first()

# Batch Operations Utility
class BatchOperations:
    """Handles batch database operations efficiently"""
    
    @staticmethod
    def bulk_insert_attendance(attendance_records):
        """
        Insert multiple attendance records efficiently
        attendance_records: List of dictionaries with attendance data
        """
        try:
            from database import Attendance
            
            bulk_records = [Attendance(**record) for record in attendance_records]
            db.bulk_save_objects(bulk_records)
            db.commit()
            return True, len(bulk_records)
        except Exception as e:
            db.rollback()
            return False, str(e)
    
    @staticmethod
    def bulk_insert_marks(marks_records):
        """
        Insert multiple marks records efficiently
        marks_records: List of dictionaries with marks data
        """
        try:
            from database import Marks
            
            bulk_records = [Marks(**record) for record in marks_records]
            db.bulk_save_objects(bulk_records)
            db.commit()
            return True, len(bulk_records)
        except Exception as e:
            db.rollback()
            return False, str(e)

# Response Pagination Helper
class Paginator:
    """Helper for paginating large result sets"""
    
    @staticmethod
    def paginate(query, page=1, per_page=20):
        """
        Paginate a query result
        Returns: (items, total, pages, current_page)
        """
        total = query.count()
        pages = (total + per_page - 1) // per_page
        
        items = query.offset((page - 1) * per_page).limit(per_page).all()
        
        return {
            'items': items,
            'total': total,
            'pages': pages,
            'current_page': page,
            'per_page': per_page,
            'has_prev': page > 1,
            'has_next': page < pages
        }

# Query Timing Utility
def time_query(f):
    """Decorator to measure query execution time"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        duration = time.time() - start
        
        print(f"Query {f.__name__} took {duration:.4f} seconds")
        return result
    return decorated_function

# Optimization Tips
OPTIMIZATION_TIPS = """
Performance Optimization Tips:

1. INDEX OPTIMIZATION:
   - Add indexes to frequently queried columns
   - Use composite indexes for multi-column queries
   
2. QUERY OPTIMIZATION:
   - Use joinedload() for eager loading of relationships
   - Avoid N+1 query problems
   - Use count() only when necessary
   - Consider using database views for complex queries
   
3. CACHING:
   - Implement query result caching
   - Cache static data that rarely changes
   - Use cache invalidation strategies
   
4. DATABASE:
   - Run VACUUM and ANALYZE regularly on SQLite
   - Use connection pooling in production
   - Archive old data to improve performance
   
5. APPLICATION:
   - Use pagination for large result sets
   - Implement lazy loading where appropriate
   - Minimize database round trips
   - Use batch operations instead of individual inserts
"""

if __name__ == "__main__":
    print(OPTIMIZATION_TIPS)
