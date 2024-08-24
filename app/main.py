from fastapi import FastAPI, Request, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from .crud import update_user_preferences

from .database import get_db
from .models import UserCreate, UserLogin, IDLink
from .crud import create_user, get_user_by_email, link_id_to_user, delete_user_and_related_data, verify_password, get_user_data_with_joins
from .auth import create_access_token, get_current_user

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/update-preferences")
async def update_preferences(
    request: Request,
    theme: str = Form(...),
    notifications: bool = Form(...),
    language: str = Form(...),
    db=Depends(get_db)
):
    current_user = get_current_user(request)
    preferences = {
        "theme": theme,
        "notifications": notifications,
        "language": language
    }
    result = update_user_preferences(db, current_user["email"], preferences)
    return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user["email"]})
    response = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db)
):
    user = UserCreate(username=username, email=email, password=password)
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = create_user(db, user)
    access_token = create_access_token(data={"sub": created_user["email"]})
    response = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@app.get("/home", response_class=HTMLResponse)
async def home(request: Request, db=Depends(get_db)):
    current_user = get_current_user(request)
    user_data = get_user_data_with_joins(db, current_user["email"])
    return templates.TemplateResponse("home.html", {"request": request, "user": user_data})

@app.post("/link-id")
async def link_id(request: Request, id: str = Form(...), db=Depends(get_db)):
    current_user = get_current_user(request)
    result = link_id_to_user(db, current_user["email"], id)
    return RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/delete-account")
async def delete_account(request: Request, db=Depends(get_db)):
    current_user = get_current_user(request)
    delete_user_and_related_data(db, current_user["email"])
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response

@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response