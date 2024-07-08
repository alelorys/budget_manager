from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from tracker.db.db import Money
from tracker.db.utils import session_scope
from tracker.api.valid_user import get_current_user
from tracker.api.validators.services import MoneyResponse,  MoneyList, Total, FileToPredict
from tracker.predict.predict import predict_budget
from tracker.consts import Consts

route = APIRouter(
    prefix='/services',
    tags=['services'],
    responses={404: {'description':'Not found'}}
)
templates = Jinja2Templates(directory=Consts.TEMPLATES_PATH)
route.mount("/static", StaticFiles(directory=Consts.STATIC_PATH), name="static")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@route.get("/list", response_model=MoneyList)
async def show_all(request: Request):
    token = request.cookies.get("Authorization")
    
    user = await get_current_user(token.replace("Bearer ",""))
    
    with session_scope() as session:
        payments = session.query(Money).filter(Money.user_id==user.id).all()
        
        
        infos = []
        if payments:
            for payment in payments:
                infos.append(MoneyResponse(
                    id=payment.id,
                    user_id=payment.user_id,
                name=payment.name,
                type='wpłata' if payment.type is True else 'wydatek',
                date=payment.date,
                amount=payment.amount,
                category=payment.category
                ))
                
            
        return templates.TemplateResponse('history.html', context={
            "request":request,
            "items":infos,
            "token":token,
            "login": user.username
        })
    
@route.get("{id}/detail/", response_model=MoneyResponse)
async def show_detail(id:int, token: str = Depends(oauth2_scheme)):
    await get_current_user(token)
    with session_scope() as session:
        payment = session.query(Money).filter(Money.id==id).first()
        
        if not payment:
            raise HTTPException(status_code=422, detail="Not found")
        
        info = MoneyResponse(
            id=payment.id,
            name=payment.name,
            type=payment.type,
            date=payment.date,
            amount=payment.amount,
            category=payment.category
        )
        return info
    
@route.get('/total', response_model=Total)
async def total(token:str = Depends(oauth2_scheme)):
    await get_current_user(token)
    with session_scope() as session:
        
        income = 0.0
        outcome = 0.0
        payments =session.query(Money).all()
        
        if not payments:
            raise HTTPException(status_code=422, detail="Not found")
        
        for payment in payments:
            if payment.type_operation == True:
                income += payment.amount
            if payment.type_operation == False:
                outcome += payment.amount
        total_amount = income - outcome
    return Total(total=total_amount)

@route.get('/predict')
async def predict(request: Request, token:str=Depends(oauth2_scheme)):
    await get_current_user(token)
    model, last_row = predict_budget()
    
    result = model.predict(last_row.values.reshape(1, -1))
    #{"przewidywana wartość": round(result[0], 2)}
    return templates.TemplateResponse("index.html", {"request":request,
                                                                "result": round(result[0], 2)})