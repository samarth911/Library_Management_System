import hashlib
from database.connection import get_connection

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate_user(username: str, password: str):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM users WHERE username=%s AND status='ACTIVE'"
            cursor.execute(query, (username,))
            user = cursor.fetchone()

            if not user:
                return None

            if user["password_hash"] == hash_password(password):
                return user
            else:
                return None
    finally:
        conn.close()
