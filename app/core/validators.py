import re

USERNAME_RE = re.compile(r"^[A-Za-z0-9_]{6,20}$")
PASSWORD_RE = re.compile(r"^[A-Za-z0-9]{8,50}$")

def validate_username_format(username: str) -> tuple[bool, str | None]:
    if not username:
        return False, "Username trống."
    if " " in username:
        return False, "Username không được có khoảng trắng."
    if len(username) < 6:
        return False, "Username phải có ít nhất 6 ký tự."
    if len(username) > 20:
        return False, "Username tối đa 20 ký tự."
    if not USERNAME_RE.fullmatch(username):
        return False, "Chỉ cho phép A–Z, a–z, 0–9, và dấu gạch dưới (_)."
    return True, None

def validate_password_format(password: str) -> tuple[bool, str | None]:
    if not password:
        return False, "Mật khẩu trống."
    if len(password) < 8 or len(password) > 50:
        return False, "Mật khẩu phải dài 8–50 ký tự."
    if not PASSWORD_RE.fullmatch(password):
        return False, "Chỉ cho phép A–Z, a–z, 0–9 (không dấu, không ký tự đặc biệt)."
    return True, None
