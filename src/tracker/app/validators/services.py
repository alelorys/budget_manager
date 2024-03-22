from pydantic import BaseModel
from datetime import datetime
from typing import List

class MoneyAdd(BaseModel):
    name: str
    type: bool
    amount: float
    category: str
    
    class Config:
        orm_mode = True
    
class MessageResponse(BaseModel):
    message: str
    
    class Config:
        orm_mode = True
    
class MoneyResponse(BaseModel):
    id: int
    name: str
    type: bool
    date: datetime
    amount: float
    category: str
    
    class Config:
        orm_mode = True
        
class MoneyList(BaseModel):
    operations: List[MoneyResponse]
    
class Total(BaseModel):
    total: float
    
    class Config:
        orm_mode = True
        
class FileToPredict(BaseModel):
    path: str