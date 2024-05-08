from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from tracker.db.db import Money
from tracker.db.utils import session_scope
from tracker.app.validators.services import MoneyResponse,  MoneyList, Total, FileToPredict
from tracker.predict.predict import predict_budget
from tracker.consts import Consts
route = APIRouter(
    prefix='/services',
    tags=['services'],
    responses={404: {'description':'Not found'}}
)
templates = Jinja2Templates(directory=Consts.TEMPLATES_PATH)
route.mount("/static", StaticFiles(directory=Consts.STATIC_PATH), name="static")

@route.get("/list", response_model=MoneyList)
def show_all(request: Request):
    with session_scope() as session:
        payments = session.query(Money).all()
        
        if not payments:
            return templates.TemplateResponse("index.html", context={"request":request})
        
        infos = []
        for payment in payments:
            infos.append(MoneyResponse(
                id=payment.id,
            name=payment.name,
            type='wpłata' if payment.type is True else 'wydatek',
            date=payment.date,
            amount=payment.amount,
            category=payment.category
            ))
            
        return templates.TemplateResponse('index.html',
                                          context={'request':request,
                                              'items':infos})
    
@route.get("/detail/{id}", response_model=MoneyResponse)
def show_detail(id:int):
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
def total():
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
def predict(request: Request):
    
    model, last_row = predict_budget()
    
    result = model.predict(last_row.values.reshape(1, -1))
    #{"przewidywana wartość": round(result[0], 2)}
    return templates.TemplateResponse("index.html", {"request":request,
                                                                "result": round(result[0], 2)})