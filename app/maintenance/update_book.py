from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from database.connection import get_connection

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get("/admin/update-book")
def update_book_page(request: Request):
    if request.session.get("role") != "ADMIN":
        return RedirectResponse("/admin-login")
    return templates.TemplateResponse("admin/update_book.html", {"request": request})


@router.post("/admin/update-book-search")
def search_book(request: Request, title: str = Form(...)):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM items WHERE title LIKE %s", (f"%{title}%",))
            books = cursor.fetchall()

            if not books:
                return templates.TemplateResponse(
                    "admin/update_book.html",
                    {"request": request, "error": "No matching book found"}
                )

        return templates.TemplateResponse(
            "admin/update_book.html",
            {"request": request, "books": books}
        )

    finally:
        conn.close()


@router.post("/admin/update-book-action")
def update_book_action(
    request: Request,
    item_id: int = Form(...),
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(...),
    rack: str = Form(...),
    category: str = Form(...)
):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE items
                SET title=%s, author=%s, publication_year=%s, rack_location=%s, category=%s
                WHERE item_id=%s
            """, (title, author, year, rack, category, item_id))

        conn.commit()

        return templates.TemplateResponse(
            "admin/update_book.html",
            {"request": request, "message": "Book updated successfully"}
        )

    finally:
        conn.close()
