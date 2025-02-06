from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class GetDate(BaseModel):
    date_from: Optional[datetime] = None
    date_to: Optional[datetime]

class GetCategories(GetDate):
    user_id: int = None
    all_categories: bool = 1

class ByCategories(BaseModel):

    category: str
    amount: float

    class Config:
        orm_mode = True

class ByCategoryList(BaseModel):
    cat_analytic: List[ByCategories] = None

    class Config:
        orm_mode = True

class GetPrediction(GetDate):
    user_id: int = None

class ByPrediction(BaseModel):
    month: str
    predicted: float
    real: float
    

class ByPredictionList(BaseModel):
    pred_analitic: List[ByPrediction] = None

class GetSummary(GetDate):
    user_id: int = None
class SummaryDetail(BaseModel):
    year: str
    income: float = 0.0
    outcome: float = 0.0
    saldo: float = 0.0

class SummaryList(BaseModel):
    summary: List[SummaryDetail]

    class Config:
        orm_mode = True