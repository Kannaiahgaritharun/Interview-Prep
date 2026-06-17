from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

from . import models, database, dependencies, auth
from .routers import auth as auth_router
from .routers import questions, progress, dashboard

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Interview Preparation Portal")

# Static files and templates
os.makedirs("app/static", exist_ok=True)
os.makedirs("app/templates", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Include API Routers
app.include_router(auth_router.router)
app.include_router(questions.router)
app.include_router(progress.router)
app.include_router(dashboard.router)

# --- Frontend Routes ---

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return RedirectResponse(url="/dashboard")

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html", context={"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request, current_user: models.User = Depends(dependencies.get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(request=request, name="dashboard.html", context={"request": request, "user": current_user})

@app.get("/questions", response_class=HTMLResponse)
def questions_page(request: Request, current_user: models.User = Depends(dependencies.get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(request=request, name="questions.html", context={"request": request, "user": current_user})

@app.get("/questions/add", response_class=HTMLResponse)
def add_question_page(request: Request, current_user: models.User = Depends(dependencies.get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(request=request, name="add_question.html", context={"request": request, "user": current_user})

@app.get("/questions/{id}", response_class=HTMLResponse)
def question_detail_page(request: Request, id: int, current_user: models.User = Depends(dependencies.get_current_user_optional)):
    if not current_user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse(request=request, name="question_detail.html", context={"request": request, "user": current_user, "question_id": id})
