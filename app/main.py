from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from auth.login_controller import router as login_router
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse



app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="library-secret-key")

templates = Jinja2Templates(directory="../templates")

app.mount("/static", StaticFiles(directory="../static"), name="static")

app.include_router(login_router)


@app.get("/")
def root():
    return {"message": "Library Management System Running"}

@app.get("/admin/home")
def admin_home(request: Request):
    if request.session.get("role") != "ADMIN":
        return RedirectResponse("/admin-login")
    return templates.TemplateResponse("admin/home.html", {"request": request})


@app.get("/user/home")
def user_home(request: Request):
    if request.session.get("role") not in ["USER", "ADMIN"]:
        return RedirectResponse("/user-login")
    return templates.TemplateResponse("user/home.html", {"request": request})


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/admin-login")
