import logging
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from tracker.db.db import Users 
from tracker.db.utils import session_scope
from tracker.api.valid_user import get_current_user, get_password_hash
from tracker.api.validators.profile import SetPassword

from tracker.consts import Consts

logging.basicConfig(level=logging.INFO)
route = APIRouter(
    prefix='/profile',
    tags=['profile'],
    responses={404:{'description':'Not found'}}
)

templates = Jinja2Templates(Consts.TEMPLATES_PATH)
route.mount('/static', StaticFiles(directory=Consts.STATIC_PATH))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@route.get('/page')
async def page(request:Request):
    token = request.cookies.get('Authorization').replace('Bearer ','')
    user = await get_current_user(token)

    response = {'request':request,
                'token':token,
                'login':user.username}
    return templates.TemplateResponse('profile.html',context=response)

@route.put("/set_pwd")
async def set_pwd(request:Request, pwd_request:SetPassword):
    token = request.cookies.get('Authorization').replace('Bearer ','')
    logging.info(token)
    user = await get_current_user(token)

    with session_scope() as session:
        user = session.query(Users).filter(Users.id==user.id).first()
        user.password = get_password_hash(pwd_request.new_pwd)

        return 200
