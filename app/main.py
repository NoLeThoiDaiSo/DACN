from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.routers import pages, auth, problems
from app.core.config import settings
from app.middlewares.session_guard import SessionGuardMiddleware

app = FastAPI(title="MLJudge")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# QUAN TRỌNG: SessionMiddleware phải chạy TRƯỚC guard
app.add_middleware(SessionGuardMiddleware)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(pages.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(problems.router, prefix="/problems", tags=["problems"])
