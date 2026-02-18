from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from datetime import date, timedelta
from database.connection import get_connection

router = APIRouter()
templates = Jinja2Templates(directory="../templates")

from fastapi.responses import RedirectResponse


@router.get("/issue-select")
def issue_select_redirect():
    return RedirectResponse("/success?msg=Book Issued Successfully", status_code=303)


@router.post("/issue-select")
def issue_select(request: Request, copy_id: int = Form(...)):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            query = """
            SELECT c.copy_id, i.title, i.author
            FROM item_copies c
            JOIN items i ON c.item_id = i.item_id
            WHERE c.copy_id=%s
            """
            cursor.execute(query, (copy_id,))
            book = cursor.fetchone()

        today = date.today()
        return_date = today + timedelta(days=15)

        return templates.TemplateResponse(
            "transactions/issue_book.html",
            {
                "request": request,
                "book": book,
                "issue_date": today,
                "return_date": return_date
            }
        )
    finally:
        conn.close()

from datetime import datetime
from fastapi.responses import RedirectResponse


@router.post("/confirm-issue")
def confirm_issue(
    request: Request,
    copy_id: int = Form(...),
    membership_no: str = Form(...),
    issue_date: str = Form(...),
    return_date: str = Form(...),
    remarks: str = Form("")
):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            # 1. find member using membership number
            cursor.execute(
                "SELECT member_id FROM members WHERE membership_no=%s AND membership_status='ACTIVE'",
                (membership_no,)
            )
            member = cursor.fetchone()

            if not member:
                return templates.TemplateResponse(
                    "transactions/issue_book.html",
                    {"request": request, "error": "Invalid or inactive membership"}
                )

            member_id = member["member_id"]

            # 2. insert issue record
            insert_issue = """
            INSERT INTO issues (copy_id, member_id, issue_date, due_date, issued_by, remarks)
            VALUES (%s,%s,%s,%s,%s,%s)
            """

            cursor.execute(insert_issue, (
                copy_id,
                member_id,
                issue_date,
                return_date,
                1,   # admin user id
                remarks
            ))

            # 3. mark copy issued
            cursor.execute(
                "UPDATE item_copies SET status='ISSUED' WHERE copy_id=%s",
                (copy_id,)
            )

        conn.commit()

        return RedirectResponse("/success?msg=Book Issued Successfully", status_code=303)

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}

    finally:
        conn.close()

