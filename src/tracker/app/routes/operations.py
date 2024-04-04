from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import  StaticFiles
from datetime import datetime
from tracker.db.utils import session_scope
from tracker.db.db import Money
from tracker.app.validators.services import MoneyAdd, MessageResponse, MoneyResponse
from tracker.consts import Consts

route = APIRouter(
    prefix='/operations',
    tags=['operations'],
    responses={404:{'description':'Not found'}}
)

templates = Jinja2Templates(directory=Consts.TEMPLATES_PATH)
route.mount("/templates", StaticFiles(directory=Consts.TEMPLATES_PATH), name="templates")

@route.get("/form")
def form(request: Request):
    return templates.TemplateResponse(name="operations.html", context={"request":request})

@route.post("/add/")
async def add(addItems: MoneyAdd):
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