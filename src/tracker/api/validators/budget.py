from pydantic import BaseModel
from typing import List, Text, Any, Union, Dict, Optional
from datetime import datetime
class Predict(BaseModel):
    predicted: float
    real: float
    date: datetime
    user_id: int

    class Config:
        orm_mode = True

class AddBudget(BaseModel):
    budget_date: datetime

class BudgetItem(BaseModel):
    budget_id: int
    category_name: str
    planned_amount: float
    real_amount: float

class AddBunch(BaseModel):
    items: List[BudgetItem] = []