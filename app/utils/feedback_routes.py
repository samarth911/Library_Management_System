from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


@router.get("/success")
def success_page(request: Request, msg: str = "Operation completed"):
    return templates.TemplateResponse(
        "shared/confirmation.html",
        {"request": request, "message": msg}
    )


@router.get("/cancel")
def cancel_page(request: Request, msg: str = "Operation cancelled"):
    return templates.TemplateResponse(
        "shared/cancellation.html",
        {"request": request, "message": msg}
    )
