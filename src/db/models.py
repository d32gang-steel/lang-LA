"""
数据库模型和操作方法
"""
from typing import List, Dict, Optional
from datetime import datetime
from .database import get_db_connection


class LearningPoint:
    """学习点数据模型"""
    
    @staticmethod
    def create(thread_id: str, topic: str, difficulty_level: str, notes: str) -> int:
        """
        创建学习点记录
        
        返回: 插入记录的ID
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = """
                INSERT INTO learning_points (thread_id, topic, difficulty_level, notes)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """
            cursor.execute(sql, (thread_id, topic, difficulty_level, notes))
            result = cursor.fetchone()
            conn.commit()
            return result['id']
    
    @staticmethod
    def get_by_thread_id(thread_id: str) -> List[Dict]:
        """根据thread_id获取所有学习点"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT id, thread_id, topic, difficulty_level, notes, created_at
                FROM learning_points
                WHERE thread_id = %s
                ORDER BY created_at DESC
            """
            cursor.execute(sql, (thread_id,))
            return cursor.fetchall()
    
    @staticmethod
    def get_by_topic(topic: str, limit: int = 100) -> List[Dict]:
        """根据知识点获取学习点"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT id, thread_id, topic, difficulty_level, notes, created_at
                FROM learning_points
                WHERE topic LIKE %s
                ORDER BY created_at DESC
                LIMIT %s
            """
            cursor.execute(sql, (f"%{topic}%", limit))
            return cursor.fetchall()
    
    @staticmethod
    def get_statistics_by_thread(thread_id: str) -> Dict:
        """获取某个线程的统计信息"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # 总记录数
            cursor.execute("SELECT COUNT(*) as total FROM learning_points WHERE thread_id = %s", (thread_id,))
            total = cursor.fetchone()['total']
            
            # 按难度统计
            cursor.execute("""
                SELECT difficulty_level, COUNT(*) as count
                FROM learning_points
                WHERE thread_id = %s
                GROUP BY difficulty_level
            """, (thread_id,))
            difficulty_stats = {row['difficulty_level']: row['count'] for row in cursor.fetchall()}
            
            # 最常见的困惑点（按topic统计）
            cursor.execute("""
                SELECT topic, COUNT(*) as count
                FROM learning_points
                WHERE thread_id = %s
                GROUP BY topic
                ORDER BY count DESC
                LIMIT 10
            """, (thread_id,))
            common_topics = cursor.fetchall()
            
            return {
                'total': total,
                'difficulty_stats': difficulty_stats,
                'common_topics': common_topics
            }
    
    @staticmethod
    def get_recent_learning_points(thread_id: str, limit: int = 20) -> List[Dict]:
        """获取最近的学习点"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT id, thread_id, topic, difficulty_level, notes, created_at
                FROM learning_points
                WHERE thread_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            """
            cursor.execute(sql, (thread_id, limit))
            return cursor.fetchall()
    
    @staticmethod
    def get_all_sessions() -> List[Dict]:
        """获取所有有学习记录的会话列表"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            sql = """
                SELECT thread_id, 
                       COUNT(*) as record_count,
                       MIN(created_at) as first_record,
                       MAX(created_at) as last_record
                FROM learning_points
                GROUP BY thread_id
                ORDER BY last_record DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()

