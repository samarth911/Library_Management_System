from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from database.connection import get_connection
from fastapi.responses import RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get("/return-book")
def return_book_page(request: Request):
    return templates.TemplateResponse("transactions/return_book.html", {"request": request})


@router.post("/return-book")
def fetch_issue(request: Request, serial_no: str = Form(...)):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            query = """
            SELECT i.issue_id, i.issue_date, i.due_date,
                   m.membership_no, m.name,
                   it.title, it.author, c.copy_id
            FROM issues i
            JOIN members m ON i.member_id = m.member_id
            JOIN item_copies c ON i.copy_id = c.copy_id
            JOIN items it ON c.item_id = it.item_id
            WHERE c.serial_no=%s AND i.status='ISSUED'
            """
            cursor.execute(query, (serial_no,))
            issue = cursor.fetchone()

            if not issue:
                return templates.TemplateResponse(
                    "transactions/return_book.html",
                    {"request": request, "error": "No active issue found for this serial number"}
                )

        return templates.TemplateResponse(
            "transactions/return_book.html",
            {"request": request, "issue": issue}
        )

    finally:
        conn.close()


from datetime import datetime, date


@router.post("/confirm-return")
def confirm_return(
    request: Request,
    issue_id: int = Form(...),
    copy_id: int = Form(...),
    return_date: str = Form(...)
):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            # get due date
            cursor.execute(
                "SELECT due_date FROM issues WHERE issue_id=%s",
                (issue_id,)
            )
            issue = cursor.fetchone()

            due_date = issue["due_date"]
            return_dt = datetime.strptime(return_date, "%Y-%m-%d").date()

            # calculate fine (₹5 per day)
            late_days = (return_dt - due_date).days
            fine = max(0, late_days * 5)

            # create fine record
            cursor.execute(
                "INSERT INTO fines(issue_id, calculated_amount) VALUES(%s,%s)",
                (issue_id, fine)
            )

        conn.commit()

        return templates.TemplateResponse(
            "transactions/pay_fine.html",
            {
                "request": request,
                "issue_id": issue_id,
                "copy_id": copy_id,
                "fine": fine
            }
        )

    finally:
        conn.close()


@router.post("/complete-return")
def complete_return(
    request: Request,
    issue_id: int = Form(...),
    copy_id: int = Form(...),
    paid: str = Form(None),
    remarks: str = Form("")
):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:

            # check fine
            cursor.execute(
                "SELECT fine_id, calculated_amount FROM fines WHERE issue_id=%s",
                (issue_id,)
            )
            fine = cursor.fetchone()

            if fine["calculated_amount"] > 0 and not paid:
                return templates.TemplateResponse(
                    "transactions/pay_fine.html",
                    {
                        "request": request,
                        "issue_id": issue_id,
                        "copy_id": copy_id,
                        "fine": fine["calculated_amount"],
                        "error": "You must confirm fine payment"
                    }
                )

            # mark fine paid
            cursor.execute(
                "UPDATE fines SET is_paid=1, paid_date=CURDATE(), remarks=%s WHERE issue_id=%s",
                (remarks, issue_id)
            )

            # update issue
            cursor.execute(
                "UPDATE issues SET status='RETURNED', return_date=CURDATE() WHERE issue_id=%s",
                (issue_id,)
            )

            # make book available again
            cursor.execute(
                "UPDATE item_copies SET status='AVAILABLE' WHERE copy_id=%s",
                (copy_id,)
            )

        conn.commit()

        return RedirectResponse("/search-book", status_code=303)

    finally:
        conn.close()
