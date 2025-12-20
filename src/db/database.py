"""
数据库连接和初始化模块
"""
import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from contextlib import contextmanager
from typing import Optional

load_dotenv()

# 数据库配置
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'dbname': os.getenv('DB_NAME', 'lang_la'),
}


@contextmanager
def get_db_connection():
    """获取数据库连接的上下文管理器"""
    conn = None
    try:
        conn = psycopg.connect(**DB_CONFIG, row_factory=dict_row)
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def init_database():
    """初始化数据库表结构"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 创建难度级别枚举类型
        cursor.execute("""
            DO $$ BEGIN
                CREATE TYPE difficulty_enum AS ENUM ('easy', 'medium', 'hard');
            EXCEPTION
                WHEN duplicate_object THEN null;
            END $$;
        """)
        
        # 创建学习点记录表
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS learning_points (
            id SERIAL PRIMARY KEY,
            thread_id VARCHAR(255) NOT NULL,
            topic VARCHAR(500) NOT NULL,
            difficulty_level difficulty_enum NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_thread_id ON learning_points(thread_id);
        CREATE INDEX IF NOT EXISTS idx_topic ON learning_points(topic);
        CREATE INDEX IF NOT EXISTS idx_difficulty ON learning_points(difficulty_level);
        CREATE INDEX IF NOT EXISTS idx_created_at ON learning_points(created_at);
        """
        
        cursor.execute(create_table_sql)
        conn.commit()
        print("数据库表初始化完成")


if __name__ == "__main__":
    init_database()

