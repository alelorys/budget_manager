from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy import and_, func

from tracker.api.valid_user import get_current_user
from tracker.db.utils import session_scope
from tracker.db.db import Models, Users
from tracker.predict import process_data, model as model_obj
from tracker.consts import Consts


# get models list
# train new model
# remove model
# activate model
route = APIRouter(
    prefix='/models',
    tags=['models'],
    responses={404:{'description':'Not found'}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@route.get('/')
async def models_list(request:Request, token:str = Depends(oauth2_scheme)):
    '''
    endpoint ma wyświetlać listę modeli, pojedynczy wiersz zawiera: nazwę modelu, datę wytrenowania/dodania oraz status.

    json pojedynczego wiersza
    {
        model_name: model_name,
        date: date,
        status: status
    }

    json listy
    [
        {
            model_name: model_name,
            date: date,
            status: status
        },
        {
            model_name: model_name,
            date: date,
            status: status
        },
    ]
    '''
    
    user = await get_current_user(token)
    with session_scope() as session:
        models = session.query(Users).filter(Users.id==user.id)\
            .join(Models, Users.model_id == Models.id).all()
        
        model_list = []
        for model in models:
            model: Models
            model_list.append({
                "model_name":model.name,
                "date": model.date,
                "status": model.state
            })
    
        return model_list

@route.delete('/delete')
async def remove_model(model_request:Request, token:str = Depends(oauth2_scheme)):
    user = await get_current_user(token)

    with session_scope() as session:
        model = session.query(Models).filter(Models.name==model_request.model_name).first()

        if not model:
            raise Exception(f'Model {model_request.model_name} not found')
        
        model = session.query(Models).filter(Models.name==model_request.model_name).delete()

        if model == 0:
            raise Exception(f'Model {model_request.model_name} not delete')
        else:
            process_data.remove_model(model_request.model_name)
            return 200
        
@route.put('/activate')       
async def activate_model(model_request:Request):
    with session_scope() as session:
        model = session.query(Models).filter(Models.name==model_request.model_name).first()

        if not model:
            raise Exception(f'Model {model_request.model_name} not found')
        
        model.state = True
        session.commit()