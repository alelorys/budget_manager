from datetime import datetime
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
    ByPredictionList)
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
@route.get("/")
async def main(request:Request):
    token = request.cookies.get('Authorization').replace('Bearer ','')
    user = await get_current_user(token)

    return templates.TemplateResponse(name='analitics.html',context={'request':request,
                                                                     'token':token,
                                                                     'user_id':user.id,
                                                                   'login':user.username})

@route.get('/categories')
async def by_categories_all(request:GetCategories,token:str=Depends(oauth2_scheme)):
    #token = request.cookies.get('Authorization').replace("Bearer ","")
    user = await get_current_user(token)
    date_from  = request.date_from 
    date_to = request.date_to
    
    with session_scope() as session:
        filters = []
        
        filters.append(Money.user_id == request.user_id)
        if date_from:
            filters.append(Money.date >= date_from)

        if date_to:
            filters.append(Money.date <= date_to)
        else:
            filters.append(Money.date <= datetime.now())

        if request.all_categories == False:
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

@route.get('/by_predictions')
async def by_predictions(request:GetPrediction, token:str=Depends(oauth2_scheme)):
    user = await get_current_user(token)

    with session_scope() as session:
        filters = []

        filters.append(Predict.user_id==request.user_id)
        if request.date_from:
            filters.append(Predict.date>=request.date_from)
        if request.date_to:
            filters.append(Predict.date<=request.date_to)
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
async def summary(request,token:str = Depends(oauth2_scheme)):
    user = await get_current_user(token)

    with session_scope() as session:
        pass