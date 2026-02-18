from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from database.connection import get_connection
from datetime import date, timedelta

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get("/admin/update-membership")
def update_membership_page(request: Request):
    if request.session.get("role") != "ADMIN":
        return RedirectResponse("/admin-login")
    return templates.TemplateResponse("admin/update_membership.html", {"request": request})


@router.post("/admin/update-membership")
def fetch_member(request: Request, membership_no: str = Form(...)):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM members WHERE membership_no=%s", (membership_no,))
            member = cursor.fetchone()

            if not member:
                return templates.TemplateResponse(
                    "admin/update_membership.html",
                    {"request": request, "error": "Membership not found"}
                )

        return templates.TemplateResponse(
            "admin/update_membership.html",
            {"request": request, "member": member}
        )

    finally:
        conn.close()


@router.post("/admin/update-membership-action")
def update_membership_action(
    request: Request,
    membership_no: str = Form(...),
    action: str = Form(...)
):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            if action == "extend":
                cursor.execute("SELECT membership_end_date FROM members WHERE membership_no=%s", (membership_no,))
                end_date = cursor.fetchone()["membership_end_date"]

                new_end = end_date + timedelta(days=180)

                cursor.execute(
                    "UPDATE members SET membership_end_date=%s WHERE membership_no=%s",
                    (new_end, membership_no)
                )

                message = "Membership extended 6 months"

            elif action == "cancel":
                cursor.execute(
                    "UPDATE members SET membership_status='CANCELLED' WHERE membership_no=%s",
                    (membership_no,)
                )
                message = "Membership cancelled"

        conn.commit()

        return templates.TemplateResponse(
            "admin/update_membership.html",
            {"request": request, "message": message}
        )

    finally:
        conn.close()
