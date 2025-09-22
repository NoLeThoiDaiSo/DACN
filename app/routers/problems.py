from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.utils.flash import pop_flash

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

# Mock problems
PROBLEMS = [
    {"id": 1, "title": "MNIST Classifier", "avg_loss": 0.142, "difficulty": "Easy",   "tags": ["cv", "ml"]},
    {"id": 2, "title": "Cats vs Dogs",     "avg_loss": 0.368, "difficulty": "Medium", "tags": ["cv", "augment"]},
    {"id": 3, "title": "Titanic Survival", "avg_loss": 0.512, "difficulty": "Easy",   "tags": ["tabular"]},
    {"id": 4, "title": "Toxic Comments",   "avg_loss": 0.893, "difficulty": "Hard",   "tags": ["nlp"]},
]

@router.get("", response_class=HTMLResponse)
def list_problems(request: Request):
    flash = pop_flash(request)
    return templates.TemplateResponse(
        "problems/list.html",
        {"request": request, "problems": PROBLEMS, "flash": flash}
    )
