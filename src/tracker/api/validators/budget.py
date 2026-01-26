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

class DeleteRequest(BaseModel):
    id: int
class AddBudget(BaseModel):
    budget_date: datetime

class CategoryItemsList(BaseModel):
    categories: Optional[List[str]] = []

    class Config:
        orm_mode = True
class EditBudgetItems(BaseModel):
    id: int
    category_name: Optional[str] = None
    planned_amount: Optional[float] = None
    real_amount: Optional[float] = None
    main: Optional[bool] = False
class BudgetItem(BaseModel):
    budget_id: int
    name: Optional[str] = None
    category_name: str
    planned_amount: float
    real_amount: Optional[float] = None
    fixed: Optional[bool] = False

class BudgetItemsList(BaseModel):
    items: Optional[List[BudgetItem]] = []

    class Config:
        orm_mode = True

class Budget(BaseModel):
    id: int
    budget_date:datetime

    class config:
        orm_mode = True

class Budgets(BaseModel):
    budgets: Optional[List[Budget]] = []