
import psycopg2
import psycopg2.extras
from psycopg2 import pool
import logging
from contextlib import contextmanager
from config import DATABASE_URL

logger = logging.getLogger(__name__)

# Connection pool
connection_pool = None

def init_connection_pool():
    global connection_pool
    try:
        # Use connection pooling optimized for Fly.io
        connection_pool = psycopg2.pool.ThreadedConnectionPool(
            1, 5,  # Smaller pool for Fly.io efficiency
            dsn=DATABASE_URL,
            sslmode='require'
        )
        logger.info("PostgreSQL connection pool initialized for Fly.io")
    except Exception as e:
        logger.error(f"Error initializing connection pool: {e}")
        raise

@contextmanager
def get_db():
    """Get database connection from pool"""
    if connection_pool is None:
        init_connection_pool()
    
    conn = None
    try:
        conn = connection_pool.getconn()
        conn.autocommit = False
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        if conn:
            connection_pool.putconn(conn)

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
            profile_pic TEXT DEFAULT NULL,
            join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            badges TEXT DEFAULT '[]',
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            verification_status INTEGER DEFAULT 0
        )""")
        
        # Verification messages table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS verification_messages (
            user_id BIGINT PRIMARY KEY,
            chat_id BIGINT,
            message_id INTEGER
        )""")
        
        # Admins table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            user_id BIGINT PRIMARY KEY
        )""")
        
        # Settings table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )""")
        
        # Reputation transactions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reputation_transactions (
            id SERIAL PRIMARY KEY,
            from_user_id BIGINT,
            to_user_id BIGINT NOT NULL,
            chat_id BIGINT,
            amount INTEGER DEFAULT 1,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reason TEXT
        )""")
        
        # Loans table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            loan_id TEXT PRIMARY KEY,
            user_id BIGINT NOT NULL,
            username TEXT,
            chat_id BIGINT,
            amount DECIMAL(10,2) NOT NULL,
            interest_rate DECIMAL(5,4) NOT NULL,
            total_due DECIMAL(10,2) NOT NULL,
            status TEXT DEFAULT 'pending',
            request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_date TIMESTAMP,
            approval_date TIMESTAMP,
            repayment_date TIMESTAMP,
            admin_id BIGINT,
            level TEXT
        )""")
        
        # Create indexes for better performance
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_users_total_rep ON users(total_rep DESC);
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_reputation_transactions_to_user ON reputation_transactions(to_user_id);
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_loans_user_id ON loans(user_id);
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_loans_status ON loans(status);
        """)
        
        logger.info("Database tables initialized successfully")

def close_connection_pool():
    """Close the connection pool"""
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        logger.info("Connection pool closed")
      
