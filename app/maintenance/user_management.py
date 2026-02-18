from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from database.connection import get_connection
import hashlib

router = APIRouter()
templates = Jinja2Templates(directory="../templates")


def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


@router.get("/admin/user-management")
def user_management_page(request: Request):
    if request.session.get("role") != "ADMIN":
        return RedirectResponse("/admin-login")
    return templates.TemplateResponse("admin/user_management.html", {"request": request})


# ---------- CREATE NEW USER ----------
@router.post("/admin/create-user")
def create_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            if cursor.fetchone():
                return templates.TemplateResponse(
                    "admin/user_management.html",
                    {"request": request, "error": "User already exists"}
                )

            cursor.execute(
                "INSERT INTO users(username, password_hash, role) VALUES(%s,%s,'USER')",
                (username, hash_password(password))
            )

        conn.commit()

        return templates.TemplateResponse(
            "admin/user_management.html",
            {"request": request, "message": "User created successfully"}
        )

    finally:
        conn.close()


# ---------- SEARCH EXISTING USER ----------
@router.post("/admin/search-user")
def search_user(request: Request, username: str = Form(...)):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT username, status FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()

            if not user:
                return templates.TemplateResponse(
                    "admin/user_management.html",
                    {"request": request, "error": "User not found"}
                )

        return templates.TemplateResponse(
            "admin/user_management.html",
            {"request": request, "found_user": user}
        )

    finally:
        conn.close()


# ---------- UPDATE STATUS ----------
@router.post("/admin/update-user-status")
def update_user_status(
    request: Request,
    username: str = Form(...),
    status: str = Form(...)
):
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET status=%s WHERE username=%s",
                (status, username)
            )

        conn.commit()

        return templates.TemplateResponse(
            "admin/user_management.html",
            {"request": request, "message": "User status updated"}
        )

    finally:
        conn.close()
