from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class MoneyAdd(BaseModel):
    user_id: int
    name: Optional[str] = None
    type: Optional[bool] = False
    amount: Optional[float] = None
    category: Optional[str] = None
    
    class Config:
        orm_mode = True
    
class MessageResponse(BaseModel):
    message: str
    
    class Config:
        orm_mode = True
    
class MoneyResponse(BaseModel):
    id: int
    user_id: int
    name: str
    type: str
    date: datetime
    amount: float
    category: str
    
    class Config:
        orm_mode = True
        
class PredictResponse(BaseModel):
    id: int
    user_id:int
    predicted: float
    real: float
    month: str
class MoneyList(BaseModel):
    operations: List[MoneyResponse]
    predicted: List[PredictResponse]
    
        
class FileToPredict(BaseModel):
    path: str

class CategoryList(BaseModel):
    categories: List[str]