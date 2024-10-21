from datetime import datetime, timedelta, timezone
from typing import Annotated
from urllib import response
import logging
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
import uvicorn


from tracker.db.utils import session_scope


from tracker.api.routes import (
    operations, 
    services, 
    budget, 
    categories,
    profile,
    analitics)
from tracker.consts import Consts
from tracker.db.db import Users as user_db
from tracker.api.validators.services import MessageResponse
from tracker.api.validators.login import (
    User as user_valid,
    Token,
    TokenData,
    UserInDB,
    AddUser)

from tracker.api.valid_user import authenticate_user, create_access_token, get_password_hash, get_current_user
from tracker.api.valid_user import ACCESS_TOKEN_EXPIRE_MINUTES

logging.basicConfig(level=logging.INFO)
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:2345"],  # Uwaga: w produkcji określ konkretne źródła
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory=Consts.TEMPLATES_PATH)
app.mount("/static", StaticFiles(directory=Consts.STATIC_PATH), name="static")


@app.get("/register_form")
async def register_form(request:Request):
    return templates.TemplateResponse(name="register.html", context={"request":request})
@app.get("/login_form")
async def login_form(request:Request):
    return templates.TemplateResponse(name="login.html", context={"request":request})

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    with session_scope() as session:
        users = session.query(user_db).filter(user_db.login==form_data.username).first()
        user = authenticate_user(users.as_dict(), form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        token = Token(access_token=access_token, token_type="bearer")
        response = RedirectResponse(url=f'http://127.0.0.1:2345/dashboard', status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="Authorization", value=f"Bearer {token.access_token}")
        logging.info(token)
        return response
    
@app.get("/dashboard")
async def dashboard(request: Request):
    token = request.cookies.get("Authorization")
    user = await get_current_user(token.replace("Bearer ",""))
    return templates.TemplateResponse("index.html", context={
        "request":request,
        "login":user.username,
        "token":token
    })
@app.post("/register")
async def register(register: AddUser):
    with session_scope() as session:
        user = session.query(user_db).filter(user_db.login==register.username).first()
        
        if user:
            raise HTTPException(status_code=422, detail="User already exists!")
        
        try:
            new_user = user_db(
                login = register.username,
                name = register.name,
                lastname = register.lastname,
                password = get_password_hash(register.password)
            )

            session.add(new_user)
            session.commit()

            return MessageResponse(message="User add successfully")
        except HTTPException:
            raise HTTPException(status_code=422, detail="Something goes wrong")
    
app.include_router(services.route)
app.include_router(operations.route)
app.include_router(budget.route)
app.include_router(categories.route)
app.include_router(profile.route)
app.include_router(analitics.route)
if __name__ == "__main__":
    uvicorn.run('app:app',
                host='127.0.0.1',
                port=2345,
                reload=True)