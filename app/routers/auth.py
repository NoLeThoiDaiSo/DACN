from fastapi import APIRouter, Request, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.services.users import user_service
from app.utils.flash import set_flash, pop_flash
from app.core.validators import validate_username_format, validate_password_format

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    flash = pop_flash(request)
    return templates.TemplateResponse("auth/login.html", {"request": request, "flash": flash})

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if user_service.authenticate(username, password):
        request.session["user"] = username
        set_flash(request, f"Xin chào {username}!", "success")
        return RedirectResponse(url="/problems", status_code=status.HTTP_303_SEE_OTHER)
    set_flash(request, "Sai tài khoản hoặc mật khẩu", "danger")
    return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/logout")
def logout(request: Request):
    request.session.pop("user", None)
    set_flash(request, "Đã đăng xuất", "info")
    return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)



@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    flash = pop_flash(request)
    return templates.TemplateResponse("auth/register.html", {"request": request, "flash": flash})

@router.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm: str = Form(...),
):
    ok_u, msg_u = validate_username_format(username)
    if not ok_u:
        set_flash(request, f"Username không hợp lệ: {msg_u}", "warning")
        return RedirectResponse(url="/auth/register", status_code=status.HTTP_303_SEE_OTHER)

    ok_p, msg_p = validate_password_format(password)
    if not ok_p:
        set_flash(request, f"Mật khẩu không hợp lệ: {msg_p}", "warning")
        return RedirectResponse(url="/auth/register", status_code=status.HTTP_303_SEE_OTHER)

    if password != confirm:
        set_flash(request, "Mật khẩu xác nhận không khớp", "warning")
        return RedirectResponse(url="/auth/register", status_code=status.HTTP_303_SEE_OTHER)

    if not user_service.create_user(username, email, password):
        set_flash(request, "Tên tài khoản đã tồn tại", "danger")
        return RedirectResponse(url="/auth/register", status_code=status.HTTP_303_SEE_OTHER)

    set_flash(request, "Tạo tài khoản thành công. Đăng nhập nhé!", "success")
    return RedirectResponse(url="/auth/login", status_code=status.HTTP_303_SEE_OTHER)

# Realtime: check username (tồn tại + định dạng)
@router.get("/check-username", response_class=HTMLResponse)
def check_username(username: str = ""):
    # chưa nhập => không trả thông báo (frontend sẽ bật kiểm tra sau lần nhập đầu)
    if not username:
        return HTMLResponse("")
    ok_fmt, msg = validate_username_format(username)
    if not ok_fmt:
        return HTMLResponse(f"<span class='hint err'>✖ {msg}</span>")
    if user_service.exists(username):
        return HTMLResponse(f"<span class='hint err'>✖ '{username}' đã được dùng</span>")
    return HTMLResponse(f"<span class='hint ok'>✔ '{username}' còn trống</span>")
