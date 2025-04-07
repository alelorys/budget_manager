from datetime import datetime
import httpx
import json
from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy import and_, or_, func

from tracker.api.validators.analitics import (
    ByCategories, 
    GetCategories,
    ByCategoryList, 
    GetPrediction,
    ByPrediction, 
    ByPredictionList,
    SummaryDetail,
    SummaryList,
    GetSummary)
from tracker.api.valid_user import get_current_user
from tracker.db.utils import session_scope
from tracker.db.db import Money, Predict
from tracker.consts import Consts

route = APIRouter(
    prefix='/analysis',
    tags=['analysis'],
    responses={404:{'description':'Not found'}}
)

templates= Jinja2Templates(Consts.TEMPLATES_PATH)
route.mount('/static', StaticFiles(directory=Consts.STATIC_PATH), name='static')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def get_params(params:dict):
    params = dict(params)
    for param in params:
        if params[param] == 'null':
            params[param] = None
    
    return params

@route.get("/")
async def main(request:Request):
    token = request.cookies.get('Authorization').replace('Bearer ','')
    user = await get_current_user(token)

    return templates.TemplateResponse(name='analitics.html',context={'request':request,
                                                                     'token':token,
                                                                     'user_id':user.id,
                                                                   'login':user.username})
        
@route.get('/categories')
async def by_categories_all(request:Request):#,token:str=Depends(oauth2_scheme)
    token = request.cookies.get('Authorization').replace("Bearer ","")
    user = await get_current_user(token)
    params = get_params(request.query_params)
    
    with session_scope() as session:
        filters = []
        
        filters.append(Money.user_id == user.id)
        if params.get('date_from'):
            filters.append(Money.date >= params.get('date_from'))

        if params.get('date_to'):
            filters.append(Money.date <= params.get('date_to'))
        else:
            filters.append(Money.date <= datetime.now())

        if params.get("all_categories") == False:
            filters.append(Money.type=="false")

        query = session.query(Money.category,func.sum(Money.amount)).filter(and_(*filters)).group_by(Money.category)
        
        results = query.all()
        by_category_list = []
        """
        [
        {category_name:amount
        }
        ]
        """
        if results:
            for category in results:
                by_category_list.append(ByCategories(category=category[0],
                                                     amount=category[1]))
            
        return ByCategoryList(cat_analytic=by_category_list)
    """templates.TemplateResponse(name='analitics.html',context={
            'request':request,
            'token':token,
            'user_id':user.id,
            'login':user.username,
            'categories_statistics':by_category_list})
"""
@route.get('/by_predictions')
async def by_predictions(request:Request):#, token:str=Depends(oauth2_scheme)
    token = request.cookies.get('Authorization').replace('Bearer ','')
    user = await get_current_user(token)
    params = get_params(request.query_params)
    with session_scope() as session:
        filters = []

        filters.append(Predict.user_id==user.id)
        if params.get('date_from'):
            filters.append(Predict.date>=params.get('date_from'))
        if params.get('date_to'):
            filters.append(Predict.date<=params.get('date_to'))
        else:
            filters.append(Predict.date<=datetime.now())

        query = session.query(Predict.date,func.sum(Predict.predicted),func.sum(Predict.real)).filter(and_(*filters))
        result = query.group_by(Predict.date).all()
        by_predict_real_list = []

        if result:
            for row in result:
                date:datetime = row[0]
                by_predict_real_list.append(ByPrediction(
                    month= date.strftime("%B"),
                    predicted=row[1],
                    real=row[2]
                ))
        return ByPredictionList(pred_analitic=by_predict_real_list)

@route.get("/summary")
async def summary(request:Request):#,token:str = Depends(oauth2_scheme)
    token = request.cookies.get('Authorization').replace('Bearer ','')
    user = await get_current_user(token)
    params = get_params(request.query_params)
    print("data do:",params.get('date_to'))
    with session_scope() as session:
        filters = []

        filters.append(Money.user_id==user.id)
        if params.get('date_from'):
            filters.append(Money.date>=params.get('date_from'))
        if params.get('date_to'):
            filters.append(Money.date<=params.get('date_to'))
            date = params.get('date_to').split("-")[0]
        else:
            filters.append(Money.date<=datetime.now())
            date = datetime.now().year
        
        income_query = session.query(func.sum(Money.amount))\
        .filter(Money.type=="true").filter(and_(*filters))\
        .all()[0][0]

        outcome_query = session.query(func.sum(Money.amount))\
        .filter(Money.type == 'false').filter(and_(*filters))\
        .all()[0][0]

        saldo = income_query - outcome_query
        
        detail = SummaryDetail(
            year=str(date),
            income=round(income_query, 2),
            outcome=round(outcome_query,2),
            saldo=round(saldo, 2)
                        )
            
        response = SummaryList(
            summary=[detail]
        )
    
    return response
        
