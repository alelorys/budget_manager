from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
import uvicorn


from tracker.db.utils import session_scope


from tracker.api.routes import operations, services
from tracker.consts import Consts
from tracker.db.db import Users as user_db
from tracker.api.validators.services import MessageResponse
from tracker.api.validators.login import (
    User as user_valid,
    Token,
    TokenData,
    UserInDB,
    AddUser)

from tracker.api.valid_user import authenticate_user, create_access_token, get_password_hash
from tracker.api.valid_user import ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Uwaga: w produkcji określ konkretne źródła
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
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    with session_scope() as session:
        users = session.query(user_db).all()
        user = authenticate_user(users, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.login}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    
@app.post("/register")
async def register(register: AddUser):
    with session_scope() as session:
        user = session.query(user_db).filter(user_db.login==register.login).first()
        if user:
            raise HTTPException(status_code=422, detail="User already exists!")
        
        try:
            new_user = user_db(
                login = register.login,
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
#app.include_router(operations.route)
if __name__ == "__main__":
    uvicorn.run('app:app',
                host='127.0.0.1',
                port=2345,
                reload=True)