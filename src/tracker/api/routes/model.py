from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy import and_, func

from tracker.api.valid_user import get_current_user
from tracker.db.utils import session_scope
from tracker.db.db import Models, Users
from tracker.api.validators.models import DeleteModel, ActivateModel, ModelInfo, ModelList
from tracker.predict import process_data, model as model_obj
from tracker.consts import Consts

from tracker.api.validators.services import MessageResponse


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
        models = session.query(Models).filter(Models.user_id==user.id).all()
        
        model_list = []
        for model in models:
            
            model_list.append({
                "id":model.id,
                "model_name":model.name,
                "date":model.date,
                "status":model.state
            })
    
        return model_list

@route.delete('/delete/{id}')
async def remove_model(id:int, token:str = Depends(oauth2_scheme)):
    user = await get_current_user(token)

    with session_scope() as session:
        model = session.query(Models).filter(Models.id==id).first() 
        model_path = model.model_path
        if not model:
            raise Exception(f'Model {id} not found')
        
        model = session.query(Models).filter(Models.id==id).delete()

        if model == 0:
            raise Exception(f'Model {id} not delete')
        else:
            process_data.remove_model(model_path)
            return 200
        
@route.put('/activate/{id}')       
async def activate_model(id:int,token:str = Depends(oauth2_scheme)):
    user = await get_current_user(token)
    with session_scope() as session:
        model = session.query(Models).filter(Models.id==id).first()

        if not model:
            raise Exception(f'Model {id} not found')
        
        model.state = True
        session.commit()
        return MessageResponse(message="Model activated")

@route.options("/train")
async def train_model(token:str = Depends(oauth2_scheme)):
    '''
    1. pobieramy dane w tym przypadku z pliku
    2. przetwarzanie danych
    3. zainicjowanie modelu
    4. trenowanie modelu 
    5. zapisanie modelu
        - zapisanie do pliku
        - zapisanie do bazy
            {
            name: model_name,
            date: date,
            state: None
            }
    '''
    user = await get_current_user(token)
    df = process_data.load_data_from_file()
    df = process_data.prepare_data(data=df, from_file=True)

    builded_model:model_obj.Model = model_obj.Model.build_model()
    # trenowanie modelu
    train:model_obj.Model = model_obj.Model.train_model(model=builded_model, data=df)

    # zapisanie modelu
    save_dict = model_obj.Model.save_model(model=train)

    with session_scope() as session:
        new_model = Models(
            name = save_dict['model_name'],
            date = save_dict['date'],
            state = None,
            model_path = save_dict['model_path'],
            user_id = user.id
        )

        session.add(new_model)
        session.commit
    
    return MessageResponse(message="New model training succeed")



