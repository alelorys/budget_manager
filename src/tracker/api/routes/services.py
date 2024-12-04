import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from tracker.db.db import Money, Predict
from tracker.db.utils import session_scope
from tracker.api.valid_user import get_current_user
from tracker.api.validators.services import (
    MoneyResponse,  
    MoneyList,
    PredictResponse)
from tracker.consts import Consts

logging.basicConfig(level=logging.INFO)
route = APIRouter(
    prefix='/services',
    tags=['services'],
    responses={404: {'description':'Not found'}}
)
templates = Jinja2Templates(directory=Consts.TEMPLATES_PATH)
route.mount("/static", StaticFiles(directory=Consts.STATIC_PATH), name="static")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@route.get("/list", response_model=MoneyList)
async def show_all(request: Request):
    token = request.cookies.get("Authorization")
    
    user = await get_current_user(token.replace("Bearer ",""))
    
    with session_scope() as session:
        payments = session.query(Money).filter(Money.user_id==user.id).all()
        predicted = session.query(Predict).filter(Predict.user_id==user.id).all()
        
        payments_list, predicted_list = [],[]
        if payments:
            for payment in payments:
                payments_list.append(MoneyResponse(
                    id=payment.id,
                    user_id=payment.user_id,
                name=payment.name,
                type='wpłata' if payment.type == 'true' else 'wydatek',
                date=payment.date,
                amount=payment.amount,
                category=payment.category
                ))
        if predicted:
            for predict in predicted:
                date:datetime = predict.date
                predicted_list.append(PredictResponse(
                    id=predict.id,
                    user_id=predict.user_id,
                    predicted=round(predict.predicted, 2),
                    real=round(predict.real, 2),
                    month=date.strftime("%B")
                ))       
            
        return templates.TemplateResponse('history.html', context={
            "request":request,
            "payments_list":payments_list,
            "predicted_list":predicted_list,
            "token":token,
            "login": user.username
        })
    
@route.get("{id}/detail/", response_model=MoneyResponse)
async def show_detail(id:int, token: str = Depends(oauth2_scheme)):
    await get_current_user(token)
    with session_scope() as session:
        payment = session.query(Money).filter(Money.id==id).first()
        
        if not payment:
            raise HTTPException(status_code=422, detail="Not found")
        
        info = MoneyResponse(
            id=payment.id,
            name=payment.name,
            type=payment.type,
            date=payment.date,
            amount=payment.amount,
            category=payment.category
        )
        return info
    

