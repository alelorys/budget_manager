from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import  StaticFiles
from datetime import datetime
from tracker.db.utils import session_scope
from tracker.db.db import Money, Users
from tracker.api.valid_user import get_current_user
from tracker.api.validators.services import MoneyAdd, MessageResponse, MoneyResponse
from tracker.api.validators.login import User
from tracker.consts import Consts

from jose import jwt

route = APIRouter(
    prefix='/operations',
    tags=['operations'],
    responses={404:{'description':'Not found'}}
)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
templates = Jinja2Templates(directory=Consts.TEMPLATES_PATH)
route.mount("/static", StaticFiles(directory=Consts.STATIC_PATH), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
@route.get("/form")
async def form(request: Request):
    token = request.cookies.get("Authorization")
    token = token.replace("Bearer ","")

    user = await get_current_user(token)
   
    return templates.TemplateResponse(name="operations.html", context={"request":request,
                                                                       "token":token,
                                                                       "user_id":user.id,
                                                                       "login":user.username})

@route.post("/add/")
async def add(addItems: MoneyAdd):
    
    try:
        with session_scope() as session:
            new_operation = Money(
                user_id = addItems.user_id,
                name = addItems.name,
                type = addItems.type,
                date = datetime.now(),
                amount = addItems.amount,
                category = addItems.category
            )
            session.add(new_operation)
            session.commit()
            
        return MessageResponse(message="Add payment successfully")
    except HTTPException:
        raise HTTPException(status_code=422, detail="Something goes wrong")