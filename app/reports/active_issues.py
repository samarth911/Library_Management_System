from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from reports.reports_service import get_active_issues

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get("/reports/active-issues")
def active_issues(request: Request):
    if not request.session.get("role"):
        return RedirectResponse("/admin-login")

    issues = get_active_issues()

    if request.session.get("role") == "ADMIN":
        page = "admin/reports/active_issues.html"
    else:
        page = "user/reports/active_issues.html"

    return templates.TemplateResponse(page, {"request": request, "issues": issues})
