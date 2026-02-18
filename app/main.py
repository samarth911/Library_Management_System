from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse

# existing routers
from auth.login_controller import router as login_router
from maintenance.add_membership import router as add_membership_router
from maintenance.add_book import router as add_book_router
from transactions.search_book import router as search_router
from transactions.issue_book import router as issue_router
from transactions.return_book import router as return_router
from reports.master_list import router as master_router
from reports.active_issues import router as active_router



app = FastAPI()

# session middleware
app.add_middleware(SessionMiddleware, secret_key="library-secret-key")

templates = Jinja2Templates(directory="../templates")
app.mount("/static", StaticFiles(directory="../static"), name="static")

# ROUTERS (all together here)
app.include_router(login_router)
app.include_router(add_membership_router)
app.include_router(add_book_router)
app.include_router(search_router)
app.include_router(issue_router)
app.include_router(return_router)
app.include_router(master_router)
app.include_router(active_router)


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
