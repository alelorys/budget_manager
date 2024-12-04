import calendar
import pandas as pd
from datetime import datetime, date
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from tracker.api.validators.services import MoneyResponse
from tracker.db.utils import session_scope
from tracker.db.db import Money, Predict
from tracker.api.valid_user import get_current_user
from tracker.api.validators.budget import Predict as valid_predict
from tracker.consts import Consts
from sqlalchemy import and_, func
from tracker.predict.predict import train_model, get_categories_from_db

route = APIRouter(
    prefix='/budget',
    tags=['budget'],
    responses={404:{'description':'Not found'}}
)

templates = Jinja2Templates(Consts.TEMPLATES_PATH)
route.mount('/static', StaticFiles(directory=Consts.STATIC_PATH), name='static')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def get_last_month():
    year = datetime.now().year
    month = datetime.now().month
    month -= 1
    num_days = calendar.monthrange(year, month)[1]
    days = [date(year,month, day) for day in range(1,num_days+1)]

    return days

@route.get('/page')
async def page(request: Request):
    token = request.cookies.get('Authorization').replace('Bearer ','')
    user = await get_current_user(token)

    days = get_last_month()

    with session_scope() as session:
        payments = session.query(Money).filter(and_(
            Money.user_id == user.id,
            Money.date.between(days[0],days[-1]))).all()
        monthly_payments = []
        if payments:
            for payment in payments:
                monthly_payments.append(MoneyResponse(
                    id=payment.id,
                    user_id=payment.user_id,
                name=payment.name,
                type='wpłata' if payment.type == 'true' else 'wydatek',
                date=payment.date,
                amount=payment.amount,
                category=payment.category
                ))

        predict_db:Predict = session.query(Predict).filter(Predict.user_id==user.id).all()[-1]

        if predict_db:
            predict_response = valid_predict(
                predicted=round(predict_db.predicted, 2),
                real=round(predict_db.real),
                date=predict_db.date,
                user_id=predict_db.user_id
            )
            return templates.TemplateResponse(name='budget.html', context={'request':request,
                                                                   'token':token,
                                                                   'user_id':user.id,
                                                                   'login':user.username,
                                                                   'items':monthly_payments,
                                                                   'predict_response':predict_response},
                                      )
        return templates.TemplateResponse(name='budget.html', context={'request':request,
                                                                   'token':token,
                                                                   'user_id':user.id,
                                                                   'login':user.username,
                                                                   'items':monthly_payments,
                                                                   'predict_response':None})
@route.post('/predict')
async def predict(request: Request):
    token = request.cookies.get('Authorization').replace('Bearer ','')
    user = await get_current_user(token)
    
    model = train_model(user.id)
    df:pd.DataFrame = get_categories_from_db(user.id)[1]
    df.drop(columns=['Suma'], inplace=True)
    result = model.predict(df.values)
    
    days = get_last_month()
    with session_scope() as session:
        payments = session.query(Money).filter(
            and_(
                Money.user_id==user.id,
                Money.date.between(days[0],days[-1]))).all()
        
        total = sum([pay.amount for pay in payments if pay.type == 'true'])-sum([pay.amount for pay in payments if pay.type == 'false'])

        
        predicted = Predict(
            predicted= round(result[0],2),
            real= round(total, 2),
            date=datetime.now(),
            user_id= user.id
        )
        session.add(predicted)

        return templates.TemplateResponse(name='budget.html', context={'request':request,
                                                                   'token':token,
                                                                   'user_id':user.id,
                                                                   'login':user.username,
                                                                   'predict_response':predicted})

@route.get('/month_check')
async def month_check(request:Request):
    # token = request.cookies.get('Authorization').replace('Bearer ','')
    # user = await get_current_user(token)

    
    year = datetime.now().year
    month = datetime.now().month
    
    num_days = calendar.monthrange(year, month)[1]
    days = [date(year,month, day) for day in range(1,num_days+1)]


    with session_scope() as session:
        payments = session.query(Money).filter(Money.date.between(days[0],days[-1])).all()
        print(payments)