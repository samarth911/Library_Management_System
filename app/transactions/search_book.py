from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from database.connection import get_connection

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get("/search-book")
def search_page(request: Request):
    return templates.TemplateResponse("transactions/search_book.html", {"request": request})


@router.post("/search-book")
def search_book(
    request: Request,
    title: str = Form(""),
    author: str = Form(""),
    category: str = Form("")
):

    # validation → at least one field required
    if not title and not author and not category:
        return templates.TemplateResponse(
            "transactions/search_book.html",
            {"request": request, "error": "Enter at least one search field"}
        )

    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            query = """
            SELECT c.copy_id, i.title, i.author, c.serial_no
            FROM item_copies c
            JOIN items i ON c.item_id = i.item_id
            WHERE c.status='AVAILABLE'
            """

            params = []

            if title:
                query += " AND i.title LIKE %s"
                params.append(f"%{title}%")

            if author:
                query += " AND i.author LIKE %s"
                params.append(f"%{author}%")

            if category:
                query += " AND i.category=%s"
                params.append(category)

            cursor.execute(query, params)
            results = cursor.fetchall()

        return templates.TemplateResponse(
            "transactions/search_book.html",
            {"request": request, "results": results}
        )

    finally:
        conn.close()
