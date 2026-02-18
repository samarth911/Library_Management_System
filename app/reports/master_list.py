from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from reports.reports_service import get_master_books
from fastapi.responses import RedirectResponse
from reports.reports_service import get_master_members

router = APIRouter()
templates = Jinja2Templates(directory="../templates")



@router.get("/reports/members")
def master_members(request: Request):
    if not request.session.get("role"):
        return RedirectResponse("/admin-login")

    members = get_master_members()

    if request.session.get("role") == "ADMIN":
        page = "admin/reports/master_members.html"
    else:
        page = "user/reports/master_members.html"

    return templates.TemplateResponse(page, {"request": request, "members": members})


@router.get("/reports/books")
def master_books(request: Request):
    if not request.session.get("role"):
        return RedirectResponse("/admin-login")

    books = get_master_books()

    if request.session.get("role") == "ADMIN":
        page = "admin/reports/master_books.html"
    else:
        page = "user/reports/master_books.html"

    return templates.TemplateResponse(page, {"request": request, "books": books})
