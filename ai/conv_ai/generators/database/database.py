import psycopg
from psycopg.rows import dict_row
from ai.generators.database.config import db_connection


def get_db_connection():
    """Establish and return a database connection"""
    try:
        conn = psycopg.connect(db_connection, row_factory=dict_row)
        return conn
    except psycopg.Error as e:
        print(f"Database connection error: {e}")
        raise


def execute_query(query: str, params=None):
    """Execute a SQL query and return results"""
    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute(query, params or ())

            if query.strip().upper().startswith("SELECT"):
                return cur.fetchall()
            else:
                conn.commit()
                return {"rowcount": cur.rowcount}

    except psycopg.Error as e:
        print(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()