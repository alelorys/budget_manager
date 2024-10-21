from fastapi import APIRouter, Request, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy import and_, or_, func

from tracker.api.validators.analitics import ByCategories, ByCategoryList
from tracker.api.valid_user import get_current_user
from tracker.db.utils import session_scope
from tracker.db.db import Money, Predict

route = APIRouter(
    prefix='/analysis',
    tags=['analysis'],
    responses={404:{'description':'Not found'}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
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
            
            print(by_category_list)
        return ByCategoryList(cat_analytic=by_category_list)
