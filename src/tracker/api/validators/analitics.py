from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class GetDate(BaseModel):
    date_from: Optional[datetime] = None
    date_to: Optional[datetime]

class GetCategories(GetDate):
    user_id: int
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
    user_id: int

class ByPrediction(BaseModel):
    predicted: float
    real: float
    month: str

class ByPredictionList(BaseModel):
    pred_analitic: List[ByPrediction] = None