from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import  StaticFiles
from datetime import datetime
from tracker.db.utils import session_scope
from tracker.db.db import Money
from tracker.app.validators.services import MoneyAdd, MessageResponse, MoneyResponse

route = APIRouter(
    prefix='/operations',
    tags=['operations'],
    responses={404:{'description':'Not found'}}
)

templates = Jinja2Templates(directory='templates')
route.mount("/templates", StaticFiles(directory="templates"), name="templates")

@route.get("/form")
def form(request: Request):
    return templates.TemplateResponse("operations.html", {"request":request})

@route.post("/add", response_model=MessageResponse)
def add(request:MoneyAdd):
    print(request)
    try:
        with session_scope() as session:
            new_operation = Money(
                name = request.name,
                type_operation = request.type,
                date = datetime.now(),
                amount = request.amount,
                category = request.category
            )
            session.add(new_operation)
            session.commit()
            
        return MessageResponse(message="Add payment successfully")
    except HTTPException:
        raise HTTPException(status_code=422, detail="Something goes wrong")