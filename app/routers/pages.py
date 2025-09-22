from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.utils.flash import pop_flash
from app.routers.problems import PROBLEMS

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    flash = pop_flash(request)
    return templates.TemplateResponse(
        "problems/list.html",
        {"request": request, "problems": PROBLEMS, "flash": flash}
    )
