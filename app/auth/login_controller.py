from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from auth.auth_service import authenticate_user
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates(directory="../templates")

router = APIRouter()



@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = authenticate_user(username, password)

    if not user:
        return templates.TemplateResponse(
            "auth/admin_login.html",
            {"request": request, "error": "Invalid username or password"}
        )

    if user["role"] == "ADMIN":
        request.session["user"] = user["username"]
        request.session["role"] = "ADMIN"
        return RedirectResponse(url="/admin/home", status_code=303)
    else:
        request.session["user"] = user["username"]
        request.session["role"] = "USER"
        return RedirectResponse(url="/user/home", status_code=303)


@router.get("/admin-login")
def admin_login_page(request: Request):
    return templates.TemplateResponse("auth/admin_login.html", {"request": request})


@router.get("/user-login")
def user_login_page(request: Request):
    return templates.TemplateResponse("auth/user_login.html", {"request": request})
