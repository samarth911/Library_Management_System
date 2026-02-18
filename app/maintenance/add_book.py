from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from database.connection import get_connection

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get("/admin/add-book")
def add_book_page(request: Request):
    if request.session.get("role") != "ADMIN":
        return RedirectResponse("/admin-login")
    return templates.TemplateResponse("admin/add_book.html", {"request": request})


@router.post("/admin/add-book")
def create_book(
    request: Request,
    title: str = Form(...),
    author: str = Form(...),
    year: int = Form(...),
    rack: str = Form(...),
    category: str = Form(...),
    serial: str = Form(...)
):
    if request.session.get("role") != "ADMIN":
        return RedirectResponse("/admin-login")

    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            # 1. insert item
            item_query = """
            INSERT INTO items (title, author, category, publication_year, rack_location)
            VALUES (%s,%s,%s,%s,%s)
            """
            cursor.execute(item_query, (title, author, category, year, rack))

            item_id = cursor.lastrowid

            # 2. insert physical copy
            copy_query = """
            INSERT INTO item_copies (item_id, serial_no)
            VALUES (%s,%s)
            """
            cursor.execute(copy_query, (item_id, serial))

        conn.commit()

        return templates.TemplateResponse(
            "admin/add_book.html",
            {"request": request, "message": f"{category} added successfully"}
        )

    except Exception as e:
        conn.rollback()
        return templates.TemplateResponse(
            "admin/add_book.html",
            {"request": request, "error": str(e)}
        )

    finally:
        conn.close()
