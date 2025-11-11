import logging

import calendar
from typing import List
import pandas as pd
from datetime import datetime, date
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from tracker.api.validators.services import MoneyResponse
from tracker.db.utils import session_scope
from tracker.db.db import Money, Predict, Budget, BudgetItems
from tracker.api.valid_user import get_current_user
from tracker.api.validators.budget import (
    Predict as valid_predict, 
    AddBudget,
    DeleteRequest, 
    BudgetItemsList, 
    BudgetItem)
from tracker.consts import Consts
from sqlalchemy import and_, func

logging.basicConfig(level=logging.info)

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
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1 
    num_days = calendar.monthrange(year, month)[1]
    days = [date(year,month, day) for day in range(1,num_days+1)]

    return days

@route.get('/page')
async def page(request: Request):
    token = request.cookies.get('Authorization').replace('Bearer ','')
    user = await get_current_user(token)

    days = get_last_month()
    print(days)
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

@route.get('/list/{budget_date}', response_model=BudgetItemsList)
async def list(budget_date:datetime, token:str = Depends(oauth2_scheme)):
    user = await get_current_user(token)
    
    budget_date = budget_date.strftime('%Y-%m-%d %H:%M:%S')
    with session_scope() as session:
        budget_items = session.query(BudgetItems.budget_id,
                                     BudgetItems.category_name,
                                     BudgetItems.planned_value,
                                     BudgetItems.real_value)\
            .join(Budget, BudgetItems.budget_id==Budget.id)\
        .where(Budget.budget_date == budget_date).all()

        if not budget_items:
            return  {'month':budget_date, 'items': []}
        budget_items_list = [{'budget_id':budget_id,
                              'category_name':category_name,
                              'planned_amount':planned_value,
                              'real_amount':real_value} for budget_id, category_name, planned_value, real_value in budget_items]
        
        response = {'month':budget_date, 'items':budget_items_list}
        
        return response


@route.delete('/delete')
async def delete_budget(delete_request:DeleteRequest, token:str=Depends(oauth2_scheme)):
    user = await get_current_user(token)

    with session_scope() as session:
        budget = session.query(Budget).filter(Budget.id == delete_request.id).first()
        msg = {}
        if not budget:
            raise HTTPException(status_code=404, detail='Budget not found')
        
        budget_items = session.query(BudgetItems).filter(BudgetItems.budget_id == delete_request.id).all()

        if len(budget_items) > 0:
            budget_items = session.query(BudgetItems).filter(BudgetItems.budget_id == delete_request.id).delete()
            msg["message items"] = "All items for this budget got removed"

        status = session.query(Budget).filter(Budget.id == delete_request.id).delete()

        if status == 0:
            raise HTTPException(status_code=421, detail='Budget not deleted')
        else:
            msg["message"] = "Budget succesfully removed"
            return msg

@route.post('/plan_budget')
async def plan_budget(budget_request:AddBudget,token:str = Depends(oauth2_scheme)):
    user = await get_current_user(token)

    with session_scope() as session:
        budget = session.query(Budget).filter(Budget.budget_date == budget_request.budget_date).first()

        if budget:
            raise HTTPException(status_code=422, detail="Budget is planned for this month")
        
        new_budget: Budget = Budget(
            budget_date = budget_request.budget_date
        )

        session.add(new_budget)
        session.commit()

@route.post('/plan_budget/items')
async def plan_budget_items(budget_items_request: List[BudgetItem], token:str = Depends(oauth2_scheme)):
    user = await get_current_user(token)

    with session_scope() as session:
        logging.info(f"cos{budget_items_request[0]}")
        budget = session.query(Budget).filter((Budget.id == budget_items_request[0].budget_id)).first()

        if not budget:
            raise HTTPException(status_code=422, detail=f'Budget {budget.id} not found')
       
        new_items = []
        for row in budget_items_request:
            row: BudgetItem
            new_item = BudgetItems(budget_id = row.budget_id,
                                   category_name = row.category_name,
                                   planned_value = row.planned_amount,
                                   real_value = row.real_amount)
            
            new_items.append(new_item)
        
        session.bulk_save_objects(new_items)
        session.commit()

@route.delete('/plan_budget/delete_items')
async def delete_items(delete_request:DeleteRequest, token:str=Depends(oauth2_scheme)):
    user = await get_current_user(token)

    with session_scope() as session:
        budget_item = session.query(BudgetItems).filter(BudgetItems.id == delete_request.id).first()

        if not budget_item:
            raise HTTPException(status_code=404, detail='Item not found')
        
        status = session.query(BudgetItems).filter(BudgetItems.id == delete_request.id).delete()

        if status == 0:
            raise HTTPException(status_code=421, detail='Item not removed')
        else:
            return {'message':'Item succesfully removed'}
# @route.post('/predict')
# async def predict(request: Request):
#     token = request.cookies.get('Authorization').replace('Bearer ','')
#     user = await get_current_user(token)
    
#     model = train_model(user.id)
#     df:pd.DataFrame = get_categories_from_db(user.id)[1]
#     df.drop(columns=['Suma'], inplace=True)
#     result = model.predict(df.values)
    
#     days = get_last_month()
#     with session_scope() as session:
#         payments = session.query(Money).filter(
#             and_(
#                 Money.user_id==user.id,
#                 Money.date.between(days[0],days[-1]))).all()
        
#         total = sum([pay.amount for pay in payments if pay.type == 'true'])-sum([pay.amount for pay in payments if pay.type == 'false'])

        
#         predicted = Predict(
#             predicted= round(result[0],2),
#             real= round(total, 2),
#             date=datetime.now(),
#             user_id= user.id
#         )
#         session.add(predicted)

#         return templates.TemplateResponse(name='budget.html', context={'request':request,
#                                                                    'token':token,
#                                                                    'user_id':user.id,
#                                                                    'login':user.username,
#                                                                    'predict_response':predicted})

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