from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from fastapi import Form
from datetime import date, timedelta
from database.connection import get_connection


router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get("/admin/add-membership")
def add_membership_page(request: Request):
    if request.session.get("role") != "ADMIN":
        return RedirectResponse("/admin-login")
    return templates.TemplateResponse("admin/add_membership.html", {"request": request})



@router.post("/admin/add-membership")
def create_membership(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    duration: int = Form(...)
):
    if request.session.get("role") != "ADMIN":
        return RedirectResponse("/admin-login")

    try:
        conn = get_connection()
        with conn.cursor() as cursor:

            # generate membership number
            cursor.execute("SELECT COUNT(*) as count FROM members")
            count = cursor.fetchone()["count"] + 1
            membership_no = f"M{1000 + count}"

            start_date = date.today()
            end_date = start_date + timedelta(days=30 * duration)

            query = """
            INSERT INTO members
            (membership_no, name, email, phone, address,
             membership_start_date, membership_end_date, created_by)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """

            cursor.execute(query, (
                membership_no, name, email, phone, address,
                start_date, end_date, 1
            ))

        conn.close()

        return templates.TemplateResponse(
            "admin/add_membership.html",
            {"request": request, "message": f"Membership Created: {membership_no}"}
        )

    except Exception as e:
        return templates.TemplateResponse(
            "admin/add_membership.html",
            {"request": request, "error": str(e)}
        )
