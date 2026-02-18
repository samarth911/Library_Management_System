from database.connection import get_connection
from datetime import date


def get_master_books():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            query = """
            SELECT 
                i.item_id,
                i.title,
                i.author,
                i.category,
                COUNT(c.copy_id) AS total_copies,
                SUM(CASE WHEN c.status='AVAILABLE' THEN 1 ELSE 0 END) AS available_copies
            FROM items i
            LEFT JOIN item_copies c ON i.item_id = c.item_id
            GROUP BY i.item_id, i.title, i.author, i.category
            ORDER BY i.title
            """
            cursor.execute(query)
            return cursor.fetchall()

    finally:
        conn.close()

# service function to fetch all members for master members page
def get_master_members():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            query = """
            SELECT membership_no, name, phone, membership_status, membership_end_date
            FROM members
            ORDER BY name
            """
            cursor.execute(query)
            return cursor.fetchall()

    finally:
        conn.close()

# service query to fetch all active issues for reports page
def get_active_issues():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            query = """
            SELECT 
                m.membership_no,
                m.name AS member_name,
                it.title,
                i.issue_date,
                i.due_date
            FROM issues i
            JOIN members m ON i.member_id = m.member_id
            JOIN item_copies c ON i.copy_id = c.copy_id
            JOIN items it ON c.item_id = it.item_id
            WHERE i.status='ISSUED'
            ORDER BY i.due_date
            """
            cursor.execute(query)
            return cursor.fetchall()

    finally:
        conn.close()




def get_overdue_returns():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            query = """
            SELECT 
                m.membership_no,
                m.name AS member_name,
                it.title,
                i.issue_date,
                i.due_date,
                DATEDIFF(CURDATE(), i.due_date) AS overdue_days
            FROM issues i
            JOIN members m ON i.member_id = m.member_id
            JOIN item_copies c ON i.copy_id = c.copy_id
            JOIN items it ON c.item_id = it.item_id
            WHERE i.status='ISSUED'
              AND i.due_date < CURDATE()
            ORDER BY overdue_days DESC
            """
            cursor.execute(query)
            return cursor.fetchall()

    finally:
        conn.close()
