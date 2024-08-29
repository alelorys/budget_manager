from fastapi import APIRouter, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from tracker.db.utils import session_scope
from tracker.api.valid_user import get_current_user
from tracker.api.validators.categories import CategoryList, AddCategory, DeleteCategory, EditCategory
from tracker.db.db import Category
from tracker.consts import Consts

route = APIRouter(
    prefix='/categories',
    tags=['categories'],
    responses={404:{'description':'Not found'}}
)

templates = Jinja2Templates(Consts.TEMPLATES_PATH)
route.mount('/static', StaticFiles(directory=Consts.STATIC_PATH))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@route.get('/list')
async def list(request:Request):
    token = request.cookies.get('Authorization').replace('Bearer ','')
    user = await get_current_user(token)

    with session_scope() as session:
        categories = session.query(Category).all()

        categories_list =[]
        if categories:
            for cat in categories:
                cat: Category
                categories_list.append(CategoryList(
                    id=cat.id,
                    name=cat.name
                ))


    return templates.TemplateResponse('categories.html',context={'request':request,
                                                                 'token':token,
                                                                 'user_id':user.id,
                                                                 'login':user.username,
                                                                 'categories':categories_list})

@route.post('/add')
async def add(add: AddCategory):

    with session_scope() as session:
        category = session.query(Category).filter(Category.name == add.name).first()

        if category:
            raise HTTPException(status_code=422, detail='Category already exists')
        
        new_category = Category(
            name = add.name
        )

        session.add(new_category)
        session.commit()

        return 200

@route.put('/edit')
async def edit(edit_request:EditCategory):
    with session_scope() as session:
        print(edit_request)
        category = session.query(Category).filter(Category.id == edit_request.id).first()

        if not category:
            raise HTTPException(status_code=422, detail='Not found')

        category.name = edit_request.name
    
    return 200

@route.delete('/delete')
async def delete(delete:DeleteCategory):
    with session_scope() as session:

        category = session.query(Category).filter(Category.id == delete.id).first()

        if not category:
            raise HTTPException(status_code=422, detail='Category not found')
        
        status = session.query(Category).filter(Category.id==delete.id).delete()

        if status == 0:
            return 422
        else:
            return 200
