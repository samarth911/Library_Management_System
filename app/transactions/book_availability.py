from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from database.connection import get_connection

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get("/book-availability")
def book_availability(request: Request):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            query = """
            SELECT i.title, i.author, c.serial_no
            FROM item_copies c
            JOIN items i ON c.item_id = i.item_id
            WHERE c.status='AVAILABLE'
            ORDER BY i.title
            """
            cursor.execute(query)
            books = cursor.fetchall()

        return templates.TemplateResponse(
            "transactions/book_availability.html",
            {"request": request, "books": books}
        )

    finally:
        conn.close()
