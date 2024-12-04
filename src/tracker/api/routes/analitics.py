from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy import and_, or_, func

from tracker.api.validators.analitics import ByCategories, ByCategoryList, ByPrediction, ByPredictionList
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
async def by_categories_all(request:Request,token:str=Depends(oauth2_scheme)):
    #token = request.cookies.get('Authorization').replace("Bearer ","")
    user = await get_current_user(token)

    with session_scope() as session:
        expences_by_category = session.query(Money.category, func.sum(Money.amount))\
        .filter(Money.user_id==user.id)\
        .group_by(Money.category).all()

        by_category_list = []
        """
        [
        {category_name:amount}
        ]
        """
        if expences_by_category:
            for category in expences_by_category:
                by_category_list.append(ByCategories(category=category[0],
                                                     amount=category[1]))
            
        return ByCategoryList(cat_analytic=by_category_list)

@route.get('/by_predictions')
async def by_predictions(request:Request, token:str=Depends(oauth2_scheme)):
    user = await get_current_user(token)

    with session_scope() as session:
        predict_real = session.query(func.sum(Predict.predicted), func.sum(Predict.real))\
        .filter(Predict.user_id==user.id)\
            .group_by(Predict.real).all()
        
        by_predict_real_list = []

        if predict_real:
            for row in predict_real:
                by_predict_real_list.append(ByPrediction(
                    predicted=row[0],
                    real=row[1]
                ))
        return ByPredictionList(pred_analitic=by_predict_real_list)
