from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from reports.reports_service import get_overdue_returns

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get("/reports/overdue")
def overdue_returns(request: Request):
    if not request.session.get("role"):
        return RedirectResponse("/admin-login")

    data = get_overdue_returns()

    if request.session.get("role") == "ADMIN":
        page = "admin/reports/overdue_returns.html"
    else:
        page = "user/reports/overdue_returns.html"

    return templates.TemplateResponse(page, {"request": request, "records": data})
