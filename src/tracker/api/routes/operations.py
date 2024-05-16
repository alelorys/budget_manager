from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import  StaticFiles
from datetime import datetime
from tracker.db.utils import session_scope
from tracker.db.db import Money
from tracker.api.valid_user import get_current_user
from tracker.api.validators.services import MoneyAdd, MessageResponse, MoneyResponse
from tracker.consts import Consts

route = APIRouter(
    prefix='/operations',
    tags=['operations'],
    responses={404:{'description':'Not found'}}
)

templates = Jinja2Templates(directory=Consts.TEMPLATES_PATH)
route.mount("/static", StaticFiles(directory=Consts.STATIC_PATH), name="static")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
@route.get("/form")
async def form(request: Request, token: str = Depends(oauth2_scheme)):
    await get_current_user(token)
    return templates.TemplateResponse(name="operations.html", context={"request":request})

@route.post("/add/")
async def add(addItems: MoneyAdd, token:str = Depends(oauth2_scheme)):
    await get_current_user(token)
    try:
        with session_scope() as session:
            new_operation = Money(
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