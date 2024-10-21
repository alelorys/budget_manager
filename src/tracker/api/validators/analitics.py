from pydantic import BaseModel
from typing import List, Dict

class ByCategories(BaseModel):
    category: str
    amount: float

    class Config:
        orm_mode = True

class ByCategoryList(BaseModel):
    cat_analytic: List[ByCategories] = None

    class Config:
        orm_mode = True