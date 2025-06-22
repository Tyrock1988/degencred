import sqlite3
import psycopg2
import os
import logging
from contextlib import contextmanager
from datetime import datetime
import json
from .config import DATABASE_URL, ADMIN_IDS

logger = logging.getLogger(__name__)

@contextmanager
def get_db():
    """Get database connection"""
    if DATABASE_URL:
        # Production: PostgreSQL
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        try:
            yield conn
        finally:
            conn.close()
    else:
        # Local: SQLite
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect("data/degencred.db")
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

def init_db():
    """Initialize database tables"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            username TEXT,
            total_rep INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            access_fee_paid INTEGER DEFAULT 0,
            access_fee_paid_date TIMESTAMP
        )""")
        
        # Access fee submissions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_fee_submissions (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            tx_id TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending'
        )""")
        
        # Admins table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            user_id BIGINT PRIMARY KEY
        )""")
        
        # Insert admin users
        for admin_id in ADMIN_IDS:
            if DATABASE_URL:
                cursor.execute("INSERT INTO admins (user_id) VALUES (%s) ON CONFLICT DO NOTHING", (admin_id,))
            else:
                cursor.execute("INSERT OR IGNORE INTO admins (user_id) VALUES (?)", (admin_id,))
        
        if not DATABASE_URL:
            conn.commit()
        
        logger.info("✅ Database initialized")

def get_or_create_user(user_id: int, username: str) -> dict:
    """Get or create user"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        if DATABASE_URL:
            cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        else:
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        
        user = cursor.fetchone()
        
        if not user:
            current_time = datetime.now()
            if DATABASE_URL:
                cursor.execute("""
                INSERT INTO users (user_id, username, join_date, last_active)
                VALUES (%s, %s, %s, %s)
                """, (user_id, username, current_time, current_time))
                cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
            else:
                cursor.execute("""
                INSERT INTO users (user_id, username, join_date, last_active)
                VALUES (?, ?, ?, ?)
                """, (user_id, username, current_time.isoformat(), current_time.isoformat()))
                conn.commit()
                cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = cursor.fetchone()
        
        return dict(user) if user else {}

def has_paid_access_fee(user_id: int) -> bool:
    """Check if user paid access fee"""
    with get_db() as conn:
        cursor = conn.cursor()
        if DATABASE_URL:
            cursor.execute("SELECT access_fee_paid FROM users WHERE user_id = %s", (user_id,))
        else:
            cursor.execute("SELECT access_fee_paid FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        return result and result['access_fee_paid'] == 1

def mark_access_fee_paid(user_id: int):
    """Mark access fee as paid"""
    with get_db() as conn:
        cursor = conn.cursor()
        current_time = datetime.now()
        if DATABASE_URL:
            cursor.execute("""
            UPDATE users SET access_fee_paid = 1, access_fee_paid_date = %s WHERE user_id = %s
            """, (current_time, user_id))
        else:
            cursor.execute("""
            UPDATE users SET access_fee_paid = 1, access_fee_paid_date = ? WHERE user_id = ?
            """, (current_time.isoformat(), user_id))
            conn.commit()

def store_access_fee_submission(user_id: int, tx_id: str):
    """Store access fee submission"""
    with get_db() as conn:
        cursor = conn.cursor()
        if DATABASE_URL:
            cursor.execute("""
            INSERT INTO access_fee_submissions (user_id, tx_id) VALUES (%s, %s)
            """, (user_id, tx_id))
        else:
            cursor.execute("""
            INSERT INTO access_fee_submissions (user_id, tx_id) VALUES (?, ?)
            """, (user_id, tx_id))
            conn.commit()
